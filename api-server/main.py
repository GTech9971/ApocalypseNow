"""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
macの開発環境で起動しない場合は、以下
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 
"""

from pathlib import Path

from fastapi import FastAPI, UploadFile, Response
from fastapi.responses import FileResponse
from starlette.websockets import WebSocket

import cv2
import detect_targetsite
import detect_site

from services.DetectHitPointService import DetectHitPointService
from services.ProjectiveTransform import ProjectiveTransform
from services.ImageUtils import ImageUtils

from entities.BaseResponse import BaseResponse
from entities.FetchAllTargetSiteResponse import FetchAllTargetSieResponse
from entities.UploadOriginalTargetSiteResponse import UploadOriginalTargetSiteResponse
from entities.ShootTargetSiteResponse import ShootTargetSiteResponse
from entities.DoCommandResponse import DoCommandResponse
from entities.FetchSiteCommandResponse import FetchSiteCommandResponse
from entities.FetchTargetSiteHitPointResponse import FetchTargetSiteHitPoint

from entities.DetectInfo import DetectInfo
from entities.Point import Point
from entities.TargetSite import TargetSite
from entities.TargetSiteHitPoint import TargetSiteHitPoint
from entities.UnDetectTargetSite import UnDetectTargetSite
from entities.SiteCommand import SiteCommand

from services.ap2n.TargetSitesDbService import TargetSitesDbService
from services.ap2n.TargetSiteHitPointsDbService import TargetSiteHitPointsDbService
from services.ap2n.UnDetectTargetSitesDbService import UnDetectTargetSitesDbService
from services.ap2n.SiteCommandsDbService import SiteCommandsDbService

FILE = Path(__file__).resolve()
# api-server root directory
ROOT = FILE.parents[0]

# アップロードされた画像データ
UPLOAD_PREVIEW_IMAGE_PATH = Path(
    ROOT, "upload", "preview", "preview-image.jpg")
# アップロードされた的本体の画像データ
UPLOAD_TARGETSITE_PATH = Path(ROOT, "upload", "targetsite")
# アップロードされた的の画像データ
UPLOAD_SITE_PATH = Path(ROOT, "upload", "site")

# 輪郭を塗った的の画像データ
DRAW_CONTOURS_PATH = Path(ROOT, "upload", "draw")
# ヒットポイントを塗った画像データ
DRAW_HIT_POINT_PATH = Path(ROOT, "upload", "hitpoint")

# yoloで検出できなかった的画像のデータ
UNDETECT_TARGET_SITE_PATH = Path(ROOT, "undetect")

# 的本体の学習結果データ
TARGET_SITE_WEIGHT_PATH = Path(ROOT, "weights", "targetsite.pt")
# 的の学習結果データ
SITE_WEIGHT_PATH = Path(ROOT, "weights", "site.pt")

# リサイズサイズ
RESIZE_WIDTH: int = 640
RESIZE_HEIGHT: int = 640

# yolo v5 app root directory
YOLO_APP_ROOT = Path("/usr/src/app")

app = FastAPI()


@app.get("/")
def read_root():
    return BaseResponse(return_code=0, message="hello world")


@app.post("/auth")
def auth():
    """
    認証を行う TODO
    """
    return BaseResponse(return_code=0, message="hello world")


@app.get("/fetch_all_target_site")
def fetch_all_target_site():
    """
    dbに保存されているすべてのサイトを返す
    """
    targetSiteDbservice: TargetSitesDbService = TargetSitesDbService()
    site_list: list[TargetSite] = targetSiteDbservice.fetchAllTargetSite()

    return FetchAllTargetSieResponse(return_code=0, message="", target_site_list=site_list)


@app.post("/upload_preview_image")
def upload_preview_image(file: UploadFile):
    """
    プレビュー画像を保存する
    """
    # 画像ファイルの保存
    try:
        ImageUtils.saveImg(file, UPLOAD_PREVIEW_IMAGE_PATH)
        return BaseResponse(return_code=0, message="")
    except Exception as e:
        return BaseResponse(return_code=1, message=str(e))


@app.get("/fetch_preview_image")
def fetch_preview_image():
    """
    プレビュー画像を返す
    """
    if not UPLOAD_PREVIEW_IMAGE_PATH.exists():
        return Response(status_code=404)

    return FileResponse(UPLOAD_PREVIEW_IMAGE_PATH)


@app.post("/upload_original_target_site")
def upload_original_target_site(file: UploadFile):
    """
        サイトの画像を受信し、yoloを使用してサイトのみの画像に切り取る。
        サイトの情報を返す

        @input
            file                : サイトの画像 
        @return
            message     : メッセージ
            target_site : サイトの情報
    """
    targetSiteDbservice: TargetSitesDbService = TargetSitesDbService()

    # id発行
    site_id: int = targetSiteDbservice.publishSiteId()

    # 画像ファイルの保存
    save_path = Path(UPLOAD_TARGETSITE_PATH, file.filename)
    try:
        ImageUtils.saveImg(file, save_path)
    except Exception as e:
        return BaseResponse(return_code=1, message=str(e))

    # yoloで的の座標取得
    detect_targetsite.run(weights=TARGET_SITE_WEIGHT_PATH,
                          source=save_path, save_txt=True, exist_ok=True)
    # 出力結果を読み取る
    file_name: str = file.filename.replace(".png", ".txt").replace(
        ".jpg", ".txt").replace(".JPG", ".txt")
    label_path = Path(ROOT, "runs/detect/exp/labels/", file_name)

    # 未検出の場合、画像を別フォルダに保存し、dbに記録する
    if not label_path.exists():
        image: cv2.Mat = cv2.imread(save_path)
        save_path = Path(UNDETECT_TARGET_SITE_PATH, file.filename)
        cv2.imwrite(save_path, image)
        undetectTargetSite: UnDetectTargetSite = UnDetectTargetSite(
            img_path=save_path)
        unDetectTargetSitesDbService: UnDetectTargetSitesDbService = UnDetectTargetSitesDbService()
        unDetectTargetSitesDbService.record(undetectTargetSite)
        return BaseResponse(return_code=1, message="的が識別できませんでした。別の画像をアップロードしてください")

    detect_info: list[DetectInfo] = DetectInfo.loadLabels(label_path)
    detect_info: DetectInfo = detect_info[0]

    # 的のみの画像にトリミング
    image: cv2.Mat = cv2.imread(save_path)
    image = ImageUtils.trimImg(image, detect_info.rect)

    # 射影変換を行う 失敗した場合無視する
    # TODO 中身の修正 imageが帰るようにする
    # projective_transform = ProjectiveTransform(save_path, detect_info)
    # try:
    #     projective_transform.exec()
    # except Exception as e:
    #     print("射影変換失敗")
    # finally:
    #     pass

    # 固定サイズにリサイズ
    image = ImageUtils.resizeImg(
        image, width=RESIZE_WIDTH, height=RESIZE_HEIGHT)

    # 画像の際保存 & dbへパスの保存
    cv2.imwrite(save_path, image)
    targetSite: TargetSite = TargetSite(
        site_id, str(save_path), detect_info.rect)
    targetSiteDbservice.record(targetSite)

    return UploadOriginalTargetSiteResponse(return_code=0, message="", target_site=TargetSite(site_id=site_id, img_path=save_path, trim_rect=detect_info.rect))


@app.post("/shoot_target_site")
def shoot_target_site(file: UploadFile, site_id: int):
    """
        射撃後のサイトの画像を受信し、射撃座標の取得と点数をテーブルに記録し、返す
        @param
            file            : 射撃後の画像 
            site_id         : サイトID
            site_command_id : サイトコマンドID
    """

    targetSiteDbservice: TargetSitesDbService = TargetSitesDbService()

    # サイトidが存在するか確認する
    targetSite: TargetSite = targetSiteDbservice.fetchTargetSite(
        site_id=site_id)
    if targetSite is None:
        return {"message": f"サイトid:{site_id}が存在しません"}

    # 画像ファイルの保存
    save_path = Path(UPLOAD_SITE_PATH, file.filename)
    try:
        ImageUtils.saveImg(file, save_path)
    except Exception as e:
        return BaseResponse(return_code=1, message=str(e))

    # トリミング
    image: cv2.Mat = cv2.imread(save_path)
    image = ImageUtils.trimImg(image, targetSite.getTrimRect())
    # 射影変換を行う 失敗した場合無視する
    # TODO 中身の修正 imageが帰るようにする
    # projective_transform = ProjectiveTransform(save_path, detect_info)
    # try:
    #     projective_transform.exec()
    # except Exception as e:
    #     print("射影変換失敗")
    # finally:
    #     pass

    # 固定サイズにリサイズ
    image = ImageUtils.resizeImg(
        image, width=RESIZE_WIDTH, height=RESIZE_HEIGHT)
    cv2.imwrite(save_path, image)

    # ヒットポイントの解析
    file_name: str = file.filename.replace(".png", ".txt").replace(
        ".jpg", ".txt").replace(".JPG", ".txt")
    label_path = Path(ROOT, "runs/detect/exp_site/labels/", file_name)

    # ファイルが重複するので、古いファイルを削除する
    if label_path.exists():
        label_path.rename(str(label_path) + ".old")

    # yoloでヒットポイントの座標取得
    detect_site.run(weights=SITE_WEIGHT_PATH, source=save_path,
                    name="exp_site", save_txt=True, exist_ok=True, nosave=True)

    if not label_path.exists():
        return BaseResponse(return_code=1, message="ヒットポイントが見つかりませんでした。")

    detect_list: list[DetectInfo] = DetectInfo.loadLabels(label_path)

    # yoloで取得したx,y,w,h座標から中心地の座標(x,y)に変換する
    pt_list: list[Point] = []
    for detect in detect_list:
        pt_list.append(detect.convert2CenterPoint())

    # ヒットポイントの取得を行う
    detectHitPointService: DetectHitPointService = DetectHitPointService(
        site_id=site_id)

    # 新規サイトアップロード時の画像を読み込んでヒットポイント解析に使用する
    original_image: cv2.Mat = cv2.imread(targetSite.img_path)

    hit_point_list: list[TargetSiteHitPoint] = []
    try:
        hit_point_list, img1 = detectHitPointService.detectHitInfo(
            image=original_image, pt_list=pt_list)
        # 輪郭を塗った画像の保存
        draw_save_path: Path = Path(DRAW_CONTOURS_PATH, file.filename)
        cv2.imwrite(draw_save_path, img1)

        # 射撃位置を塗った画像の保存
        hit_point_path: Path = Path(DRAW_HIT_POINT_PATH, file.filename)
        image = detectHitPointService.drawHitPoint(image, hit_point_list)
        cv2.imwrite(hit_point_path, image)
    except Exception as e:
        return BaseResponse(return_code=1, message=str(e))

    if len(hit_point_list) == 0:
        return BaseResponse(return_code=1, message="ヒットポイントが見つかりませんでした。")

    # ヒットポイント座標、ヒットポイントをtarget_site_hit_pointsテーブルに記録
    targetSiteHitPointsDbService: TargetSiteHitPointsDbService = TargetSiteHitPointsDbService()
    targetSiteHitPointsDbService.record(hit_point_list)

    # ヒット後のサイト画像パスをtarget_siteテーブルに記録
    targetSiteDbservice.recordHitImagePath(
        site_id=site_id, hit_img_path=save_path)

    return ShootTargetSiteResponse(return_code=0, message="", site_id=site_id, hit_point_list=hit_point_list)


@app.get("/fetch_target_site_hit_point")
def fetch_target_site_hit_point(site_id: int):
    """
    サイトidに一致する射撃情報を返す
    """
    targetSiteHitPointsDbService: TargetSiteHitPointsDbService = TargetSiteHitPointsDbService()
    ht_list: list[TargetSiteHitPoint] = targetSiteHitPointsDbService.fetchHitPoints(
        site_id=site_id)

    return FetchTargetSiteHitPoint(return_code=0, message="", ht_list=ht_list)


# 接続中のクライアントを識別するためのIDを格納
clients = {}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    try:
        while True:
            # クライアントからメッセージを受信
            data: str = await ws.receive_text()
            # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
            for client in clients.values():
                text: str = f"ID: {key} | Message: {data}"
                await client.send_text(text)
                print(text)
    except:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]


@app.post("/do_command")
def do_command(site_id: int, command_id: int):
    """
    サイトコマンドをdbに記録する
    site_idが未確定の場合、site_id=-1で登録する
    """
    siteCommandsDbService: SiteCommandsDbService = SiteCommandsDbService()
    site_command: SiteCommand = SiteCommand(
        id=-1, site_id=site_id, command_id=command_id)
    try:
        site_command_id: int = siteCommandsDbService.doCommand(
            site_command=site_command)
        return DoCommandResponse(return_code=0, message="", site_command_id=site_command_id)
    except Exception as e:
        return BaseResponse(return_code=1, message=str(e))


@app.get("/fetch_commands")
def fetch_command(site_id: int):
    """
    サイトコマンドをdbから取得する
    """
    siteCommandsDbService: SiteCommandsDbService = SiteCommandsDbService()
    command_list: list[SiteCommand] = siteCommandsDbService.fetchCommand(
        site_id=site_id)
    return FetchSiteCommandResponse(return_code=0, message="", command_list=command_list)


@app.post("/done_command")
def done_command(site_command_id: int, site_id: int = None):
    """
    サイトコマンドの終了処理を行う
    @params
        site_command_id : 終了するサイトコマンドid
        site_id         : 更新するターゲットサイトID(*デフォルトはNone 値が指定された場合のみ更新する)
    """
    siteCommandsDbService: SiteCommandsDbService = SiteCommandsDbService()
    siteCommandsDbService.doneCommand(
        site_command_id=site_command_id, site_id=site_id)
    return BaseResponse(return_code=0, message="")
