# start server  $uvicorn main:app --reload

from pathlib import Path

from fastapi import FastAPI, UploadFile, File

import uvicorn

import detect



FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # api-server root directory

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
        save_path = Path(ROOT, "upload", "targetsite", file.filename)
        with open(save_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"message": e}
    finally:
        file.file.close()

    # yoloで座標取得
    detect.run(weights=TARGET_SITE_WEIGHT_PATH, source=save_path, save_txt=True)
    # 出力結果を読み取る
    label_path = Path(YOLO_APP_ROOT, "runs/detect/exp/label/", file.filename.replace(".png", ".txt"))
    result = load_label(label_path)

    return {"message": f"upload success {file.filename}", "rect": result}


'''
ラベルを読み込む
'''


def load_label(path: str):
    try:
        with open(path, "r") as f:
            line = f.readline()
            return line
    except Exception as e:
        return e


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        reload=True,
        port=8000,
        log_level="debug",)