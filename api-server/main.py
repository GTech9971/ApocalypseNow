from pathlib import Path

from fastapi import FastAPI, UploadFile, File

import detect_targetsite
import detect_site
import projective_transform

from models.DetectInfo import DetectInfo
from utils.ImageUtils import trim_img, img2base64


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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload_target")
def upload_target(file: UploadFile = File(...), get_img: bool = False):
    """
        サイトの画像を受信し、yoloを使用してサイトのみの画像に切り取る。
        座標と、切り取った画像(デフォルトでは返さない)をbase64で返す

        @input
            file    : サイトの画像ファイル
            get_img : 切り取り後の画像を返す

        @return
            message : メッセージ
            rect    : x,y,w,h
            cut_img : 切り取ったサイト
    """

    # 画像ファイルの保存
    try:
        contents = file.file.read()
        save_path = Path(UPLOAD_TARGETSITE_PATH, file.filename)
        with open(save_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"message": e, "rect":None, "cut_img":None}
    finally:
        file.file.close()

    # yoloで座標取得
    detect_targetsite.run(weights=TARGET_SITE_WEIGHT_PATH,
                          source=save_path, save_txt=True, exist_ok=True)
    # 出力結果を読み取る
    label_path = Path(ROOT, "runs/detect/exp/labels/", file.filename.replace(".png", ".txt"))
    detect_info:list[DetectInfo] = load_labels(label_path)
    detect_info = detect_info[0]

    # 射影変換を行う 失敗した場合無視する
    try:
        projective_transform.exec(img_path=save_path, detect_info=detect_info)
    except Exception as e:
        print("射影変換失敗")

    if get_img:
        cut_img = trim_img(save_path, detect_info)
        base64_img:str = img2base64(cut_img)
        return {"message": f"upload success {file.filename}", "rect": detect_info.rect, "cut_img": base64_img}
    else:
        return {"message": f"upload success {file.filename}", "rect": detect_info.rect, "cut_img": None}



@app.post("/upload_site")
def upload_site(file: UploadFile = File(...)):
    """
        サイトの画像を受信し、yoloを使用して着弾位置を取得し座標で返す        

        @input
            file    : サイトの画像ファイル            

        @return
            message      : メッセージ
            rect_list    : 着弾地点の座標リスト
    """

    # 画像ファイルの保存
    try:
        contents = file.file.read()
        save_path = Path(UPLOAD_SITE_PATH, file.filename)
        with open(save_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"message": e, "rect":[]}
    finally:
        file.file.close()

    # yoloで座標取得 TODO 重複を許可していいか怪しい要チェック
    detect_site.run(weights=SITE_WEIGHT_PATH, source=save_path, name="exp_site", save_txt=True, exist_ok=True)

    # 出力結果を読み取る
    label_path = Path(ROOT, "runs/detect/exp_site/labels/", file.filename.replace(".png", ".txt"))
    detect_info:list[DetectInfo] = load_labels(label_path)
        
    return {"message": f"upload success {file.filename}", "rect_list": detect_info}



def load_labels(label_path: str)-> list[DetectInfo]:
    """
    ラベルを読み込む
    @input
        label_path  : yoloの出力結果の保存パス
    @return 
        DetectInfo  : 出力結果
    """

    detect_list:list[DetectInfo] = []

    try:
        with open(label_path, "r") as f:
            lines:list[str] = f.readlines()
            if len(lines) == 0:
                return []

            for line in lines:
                yolo_data = line[0].split(" ")
                label = int(yolo_data[0])

                x = int(yolo_data[1])
                y = int(yolo_data[2])
                w = int(yolo_data[3])
                h = int(yolo_data[4])

                detect_list.append(DetectInfo(label, x,y,w,h))

            return detect_list

    except Exception as e:
        raise e
