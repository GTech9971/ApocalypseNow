"""
find_contoursにおける輪郭の取得
https://www.learning-nao.com/?p=2020
"""

from entities.HitPoint import HitPoint
from entities.TargetSitePoint import TargetSitePoint

import cv2
from pathlib import Path


FILE = Path(__file__).resolve()
# api-server root directory
ROOT = FILE.parents[1]
DEFAULT_IMG_PATH: str = str(Path(ROOT, "resources", "sample1.png"))


class DetectHitPoint(object):
    """
    ターゲットサイトにヒットした点数を取得する
    """

    def __init__(self, site_id: int = 0, img_path: str = DEFAULT_IMG_PATH) -> None:
        self.site_id = site_id
        self.img_path = img_path

    def removeUnuseContours(self, contours: list) -> list:
        """
        不要な輪郭を削除する
        """

        # 小さな輪郭は削除する
        new_contours = []
        for i in range(0, len(contours)):
            if len(contours[i]) > 0:

                # remove small objects
                if cv2.contourArea(contours[i]) > 500:
                    new_contours.append(contours[i])

        # 一番外側の輪郭は省く
        new_contours = new_contours[1:]

        # 枠線の外側の輪郭のみに絞
        dst: list = []
        for i in range(len(new_contours)):
            if i % 2 == 0:
                dst.append(new_contours[i])

        return dst

    def detectHitInfo(self) -> str:
        """
        ヒット情報を返す
        """

        # 入力画像
        image = cv2.imread(self.img_path)
        image_copy = image.copy()

        # グレースケール化
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 閾値処理
        ret, thresh = cv2.threshold(image_gray, 95, 255, cv2.THRESH_BINARY)

        # 輪郭検出 （cv2.RETER_TREE）
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 小さい輪郭を削除して文字を消す
        contours = self.removeUnuseContours(contours)

        # ヒットポイントの設定
        pt_list: list[HitPoint] = []
        pt_list.append(HitPoint(x=124, y=126))  # 4
        pt_list.append(HitPoint(x=178, y=312))  # 7

        targetSite: TargetSitePoint = TargetSitePoint(
            site_id=self.site_id, contours=contours)
        targetSite.hit_point_list = pt_list

        info: str = targetSite.get_point_list()
        print(info)

        # 輪郭の描画
        image_1 = cv2.drawContours(image_copy, contours, -1,
                                   (0, 255, 0), 2, cv2.LINE_AA)

        # ポイントの描画
        for pt in targetSite.hit_point_list:
            image_1 = cv2.circle(image_1, pt.point(), 5, (0, 0, 255), -1)
            image_1 = cv2.putText(
                image_1, f"x={pt.x} y={pt.y}", pt.point(), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

        cv2.imwrite("./result/result.png", image_1)

        return info
