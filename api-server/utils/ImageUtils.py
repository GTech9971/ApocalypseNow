import base64
import cv2

from models.DetectInfo import DetectInfo


def trim_img(img_path: str, detect_info: DetectInfo) -> cv2.Mat:
    img: cv2.Mat = cv2.imread(img_path)

    # 画像トリミング
    x,y,w,h  = detect_info.rect    
    img = img[y:h, x:w]

    return img


def img2base64(img:cv2.Mat)->str:
    _, encodeed = cv2.imencode(".png", img)
    return base64.b64encode(encodeed).decode("ascii")