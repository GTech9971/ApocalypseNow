import cv2
import numpy as np


# 2値化
def calc_threshold(gray_img: cv2.Mat) -> int:
    luminance_percentage = 0.2
    num_threshold = gray_img.size * luminance_percentage
    flat = gray_img.flatten()

    for diff_luminance in range(100):
        if np.count_nonzero(flat > 200 - diff_luminance) >= num_threshold:
            return 200 - diff_luminance
    return 100


# 輪郭取得
def draw_countour_extraction(binary_img) -> any:
    contours, _ = cv2.findContours(
        binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)

    return cnt


# 画像の射影変換
def transform(img: cv2.Mat, cnt):
    WIDTH, HEIGHT, _ = img.shape
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    src = np.float32(list(map(lambda x: x[0], approx)))
    dst = np.float32([[0, 0], [0, WIDTH], [HEIGHT, WIDTH], [HEIGHT, 0]])

    project_matrix = cv2.getPerspectiveTransform(src, dst)

    transformed = cv2.warpPerspective(img, project_matrix, (HEIGHT, WIDTH))
    return transformed


def exec(img_path: str, rect: list):

    # load img
    img: cv2.Mat = cv2.imread(img_path)

    # 画像トリミング
    x: int = rect[1]
    y: int = rect[2]
    w: int = rect[3]
    h: int = rect[4]
    img = img[y:h, x:w]

    # グレイスケール
    gray_img: cv2.Mat = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold: int = calc_threshold(gray_img)

    # 2値化
    _, binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)

    # 輪郭抽出
    cnt = draw_countour_extraction(binary_img)

    img = transform(img, cnt)

    cv2.imwrite(img_path + "dst.png", img)
