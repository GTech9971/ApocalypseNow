from pathlib import Path

from fastapi import FastAPI, UploadFile, File

import detect_targetsite
import projective_transform


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # api-server root directory

UPLOAD_TARGETSITE_PATH = Path(
    ROOT, "upload", "targetsite")  # アップロードされた的本体の画像データ

TARGET_SITE_WEIGHT_PATH = Path(ROOT, "weights", "targetsite.pt")  # 的本体の学習結果データ
SITE_WEIGHT_PATH = Path(ROOT, "weights", "site.pt")  # 的の学習結果データ

YOLO_APP_ROOT = Path("/usr/src/app")  # yolo v5 app root directory

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload_target")
def upload_target(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        save_path = Path(UPLOAD_TARGETSITE_PATH, file.filename)
        with open(save_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"message": e}
    finally:
        file.file.close()

    # yoloで座標取得
    detect_targetsite.run(weights=TARGET_SITE_WEIGHT_PATH,
                          source=save_path, save_txt=True, exist_ok=True)
    # 出力結果を読み取る
    label_path = Path(ROOT, "runs/detect/exp/labels/",
                      file.filename.replace(".png", ".txt"))
    result = load_label(label_path)

    projective_transform.exec(img_path=save_path, rect=result)

    return {"message": f"upload success {file.filename}", "rect": result}


def load_label(label_path: str):
    'ラベルを読み込む'

    try:
        with open(label_path, "r") as f:
            result = f.readlines()
            if len(result) == 0:
                return []

            yolo_data = result[0].split(" ")
            label = int(yolo_data[0])

            x = float(yolo_data[1])
            y = float(yolo_data[2])
            w = float(yolo_data[3])
            h = float(yolo_data[4])

            return [label, x, y, w, h]

    except Exception as e:
        return e
