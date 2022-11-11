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

import MySQLdb

from services.DetectHitPointService import DetectHitPointService
from services.ProjectiveTransform import ProjectiveTransform
from services.ImageUtils import ImageUtils

from entities.DetectInfo import DetectInfo
from entities.Point import Point
from entities.TargetSite import TargetSite
from entities.TargetSiteHitPoint import TargetSiteHitPoint

from services.ap2n.TargetSitesDbService import TargetSitesDbService
from services.ap2n.TargetSiteHitPointsDbService import TargetSiteHitPointsDbService

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
    """
    mysqlに接続し、target_sites テーブルの中身を列挙する
    """
    # MySQLに接続
    conn = MySQLdb.connect(
        user='root',
        passwd='rootpass',
        host='ap2n-db',  # docker-composeのサービス名がhost名にあたる
        db='ap2n')

    # カーソルを取得
    cur = conn.cursor()

    # SQL文を実行
    sql = "SELECT * FROM target_sites;"
    cur.execute(sql)

    rows = cur.fetchall()

    # 接続をクローズ
    cur.close()
    conn.close()

    return {"tables": str(rows)}


@app.get("/test_published")
def test_publishe():
    service: TargetSitesDbService = TargetSitesDbService()
    return service.publishSiteId()


@app.get("/test_insert_targetsite")
def test_insert_targetsite():
    service: TargetSitesDbService = TargetSitesDbService()
    site_id: int = service.publishSiteId()
    save_path: str = Path(ROOT, "upload", "sample.png")
    targetSite: TargetSite = TargetSite(site_id, str(save_path))
    return service.insert(targetSite)


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
    is_new: bool = site_id is None
    targetSiteDbservice: TargetSitesDbService = TargetSitesDbService()

    # site_idがNoneの場合、id発行
    if site_id is None:
        site_id = targetSiteDbservice.publishSiteId()

    # 画像ファイルの保存
    save_path = Path(UPLOAD_TARGETSITE_PATH, file.filename)
    try:
        ImageUtils.saveImg(file=file, save_path=save_path)
    except Exception as e:
        return {"message": e}

    # yoloで的の座標取得
    detect_targetsite.run(weights=TARGET_SITE_WEIGHT_PATH,
                          source=save_path, save_txt=True, exist_ok=True)
    # 出力結果を読み取る
    label_path = Path(ROOT, "runs/detect/exp/labels/",
                      file.filename.replace(".png", ".txt"))
    if not label_path.exists():
        return {"message": "的が識別できませんでした。別の画像をアップロードしてください"}

    detect_info: list[DetectInfo] = DetectInfo.loadLabels(label_path)
    detect_info = detect_info[0]

    # 的のみの画像にトリミングして、固定サイズにリサイズ
    image: cv2.Mat = cv2.imread(save_path)
    image = ImageUtils.trimImg(image, detect_info)
    image = ImageUtils.resizeImg(image, width=640, height=640)

    # 射影変換を行う 失敗した場合無視する
    # TODO 中身の修正 imageが帰るようにする
    # projective_transform = ProjectiveTransform(save_path, detect_info)
    # try:
    #     projective_transform.exec()
    # except Exception as e:
    #     print("射影変換失敗")
    # finally:
    #     pass

    # 画像の際保存 & dbへパスの保存
    cv2.imwrite(save_path, image)
    targetSite: TargetSite = TargetSite(site_id, str(save_path))
    targetSiteDbservice.record(targetSite, is_new)

    label_path = Path(ROOT, "runs/detect/exp_site/labels/",
                      file.filename.replace(".png", ".txt"))

    # ファイルが重複するので、古いファイルを削除する
    if label_path.exists():
        label_path.rename(str(label_path) + ".old")

    # yoloでヒットポイントの座標取得
    detect_site.run(weights=SITE_WEIGHT_PATH, source=save_path,
                    name="exp_site", save_txt=True, exist_ok=True, nosave=True)

    if not label_path.exists():
        return {"message": "ヒットポイントが見つかりませんでした。"}

    detect_list: list = DetectInfo.loadLabels(label_path)

    # yoloで取得したx,y,w,h座標から中心地の座標(x,y)に変換する
    pt_list: list = []
    for detect in detect_list:
        pt_list.append(detect.convert2CenterPoint())

    # ヒットポイントの取得を行う
    detectHitPointService: DetectHitPointService = DetectHitPointService(
        site_id=site_id)
    # TODO ヒットポイントありの画像の場合、輪郭が思ったように取得できない。ヒットする前の綺麗な状態の的の画像を残しておいて使用するか？
    hit_point_list: list[TargetSiteHitPoint] = detectHitPointService.detectHitInfo(
        image=image, pt_list=pt_list)

    # TODO ヒットポイント座標と、ヒットポイントをdbに記録
    targetSiteHitPointsDbService: TargetSiteHitPointsDbService = TargetSiteHitPointsDbService()
    targetSiteHitPointsDbService.record(hit_point_list)

    return {"message": "", "site_id": site_id, "list": hit_point_list}
