import base64
import cv2

from pathlib import Path

from fastapi import UploadFile
from entities.DetectInfo import DetectInfo


class ImageUtils(object):

    def saveImg(file: UploadFile, save_path: Path):
        """
        画像ファイルの保存
        """
        try:
            contents = file.file.read()
            with open(save_path, "wb") as f:
                f.write(contents)
        except Exception as e:
            raise e
        finally:
            file.file.close()

    def trimImg(img: cv2.Mat, trim_rect: tuple) -> cv2.Mat:
        """
        画像トリミング
        """
        x, y, w, h = trim_rect
        return img[y:h, x:w]

    def resizeImg(img: cv2.Mat, width: int, height: int) -> cv2.Mat:
        """
        画像リサイズ
        """
        return cv2.resize(img, dsize=(width, height))

    def img2base64(img: cv2.Mat) -> str:
        _, encodeed = cv2.imencode(".png", img)
        return base64.b64encode(encodeed).decode("ascii")
