import cv2
import numpy as np

from entities.DetectInfo import DetectInfo
from services.ImageUtils import trim_img


class ProjectiveTransform(object):
    """
    射影変換を行う
    """

    def __init__(self, img_path: str, detect_info: DetectInfo) -> None:
        self.img_path = img_path
        self.detect_info = detect_info

    # 2値化
    def calc_threshold(self, gray_img: cv2.Mat) -> int:
        luminance_percentage = 0.2
        num_threshold = gray_img.size * luminance_percentage
        flat = gray_img.flatten()

        for diff_luminance in range(100):
            if np.count_nonzero(flat > 200 - diff_luminance) >= num_threshold:
                return 200 - diff_luminance
        return 100

    # 輪郭取得
    def draw_countour_extraction(self, binary_img) -> any:
        contours, _ = cv2.findContours(
            binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)

        return cnt

    # 画像の射影変換
    def transform(self, img: cv2.Mat, cnt):
        WIDTH, HEIGHT, _ = img.shape
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        src = np.float32(list(map(lambda x: x[0], approx)))
        dst = np.float32([[0, 0], [0, WIDTH], [HEIGHT, WIDTH], [HEIGHT, 0]])

        # 射影変換不要なレベルだとエラーで落ちる

        project_matrix = cv2.getPerspectiveTransform(src, dst)

        transformed = cv2.warpPerspective(img, project_matrix, (HEIGHT, WIDTH))
        return transformed

    def exec(self):
        # load img
        img: cv2.Mat = cv2.imread(self.img_path)

        # 画像トリミング
        img = trim_img(self.img_path, self.detect_info)

        # グレイスケール
        gray_img: cv2.Mat = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshold: int = self.calc_threshold(gray_img)

        # 2値化
        _, binary_img = cv2.threshold(
            gray_img, threshold, 255, cv2.THRESH_BINARY)

        # 輪郭抽出
        cnt = self.draw_countour_extraction(binary_img)

        img = self.transform(img, cnt)

        cv2.imwrite(self.img_path, img)
