"""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
macの開発環境で起動しない場合は、以下
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 
"""

from pathlib import Path

from fastapi import FastAPI, UploadFile, File

import cv2
import detect_targetsite
import detect_site
from services.DetectHitPointService import DetectHitPointService
from services.ProjectiveTransform import ProjectiveTransform
from services.ImageUtils import ImageUtils

from entities.DetectInfo import DetectInfo
from entities.Point import Point
from entities.TargetSiteHitPoint import TargetSiteHitPoint

from services.ap2n.TargetSitesDbService import TargetSiteDbService

FILE = Path(__file__).resolve()
# api-server root directory
ROOT = FILE.parents[0]


# アップロードされた的本体の画像データ
UPLOAD_TARGETSITE_PATH = Path(ROOT, "upload", "targetsite")
# アップロードされた的の画像データ
UPLOAD_SITE_PATH = Path(ROOT, "upload", "site")

# 的本体の学習結果データ
TARGET_SITE_WEIGHT_PATH = Path(ROOT, "weights", "targetsite.pt")
# 的の学習結果データ
SITE_WEIGHT_PATH = Path(ROOT, "weights", "site.pt")

# yolo v5 app root directory
YOLO_APP_ROOT = Path("/usr/src/app")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def test_db():
    service: TargetSiteDbService = TargetSiteDbService()
    service.publishSiteId()


@app.post("/upload_target")
def upload_target(file: UploadFile = File(...), site_id: int = None):
    """
        サイトの画像を受信し、yoloを使用してサイトのみの画像に切り取る。
        座標と、切り取った画像(デフォルトでは返さない)をbase64で返す

        @input
            file    : サイトの画像ファイル
            site_id : サイトの識別id

        @return
            message : メッセージ
            rect    : x,y,w,h
            cut_img : 切り取ったサイト
    """

    # TODO site_idがNoneの場合、発行
    if site_id == None:
        pass

    # 画像ファイルの保存
    save_path = Path(UPLOAD_TARGETSITE_PATH, file.filename)
    try:
        ImageUtils.save_img(file=file, save_path=save_path)
    except Exception as e:
        return {"message": e}

    # yoloで的の座標取得
    detect_targetsite.run(weights=TARGET_SITE_WEIGHT_PATH,
                          source=save_path, save_txt=True, exist_ok=True)
    # 出力結果を読み取る
    label_path = Path(ROOT, "runs/detect/exp/labels/",
                      file.filename.replace(".png", ".txt"))
    detect_info: list[DetectInfo] = DetectInfo.loadLabels(label_path)
    detect_info = detect_info[0]

    # 的のみの画像にトリミングして、固定サイズにリサイズ
    image: cv2.Mat = cv2.imread(save_path)
    image = ImageUtils.trimImg(image, detect_info)
    image = ImageUtils.resizeImg(image, width=640, height=640)

    # 射影変換を行う 失敗した場合無視する
    # TODO 中身の修正 imageが帰るようにする
    projective_transform = ProjectiveTransform(save_path, detect_info)
    try:
        projective_transform.exec()
    except Exception as e:
        print("射影変換失敗")
    finally:
        pass

    # 画像の際保存
    # TODO dbへパスの保存
    cv2.imwrite(save_path, image)

    # yoloでヒットポイントの座標取得 TODO 重複を許可していいか怪しい要チェック
    detect_site.run(weights=SITE_WEIGHT_PATH, source=save_path,
                    name="exp_site", save_txt=True, exist_ok=True)

    # 出力結果を読み取る
    label_path = Path(ROOT, "runs/detect/exp_site/labels/",
                      file.filename.replace(".png", ".txt"))
    detect_list: list[DetectInfo] = DetectInfo.loadLabels(label_path)

    # yoloで取得したx,y,w,h座標から中心地の座標(x,y)に変換する
    pt_list: list[Point] = []
    for detect in detect_list:
        pt_list.append(detect.convert2CenterPoint())

    # ヒットポイントの取得を行う
    detectHitPointService: DetectHitPointService = DetectHitPointService(
        site_id=site_id)

    hit_point_list: list[TargetSiteHitPoint] = detectHitPointService.detectHitInfo(
        image=image, pt_list=pt_list)

    # TODO ヒットポイント座標と、ヒットポイントをdbに記録

    return {"message": "", "site_id": site_id, "list": hit_point_list}
