"""
find_contoursにおける輪郭の取得
https://www.learning-nao.com/?p=2020
"""

from __future__ import annotations

from entities.Point import Point
from entities.TargetSiteHitPoint import TargetSiteHitPoint

from typing import Tuple
import cv2

# 最大ポイント
MAX_POINT: int = 10
# 最小ポイント
MIN_POINT: int = 4

# 輪郭の個数
CONTOURS_COUNT:int = 7


class DetectHitPointService(object):
    """
    ターゲットサイトにヒットした点数を取得する
    """

    def __init__(self, site_id: int) -> None:
        self.site_id = site_id

    def removeUnuseContours(self, contours: list) -> list:
        """
        不要な輪郭を削除する
        小さい輪郭の削除と、いちばん外側の輪郭の削除、枠線の外側の輪郭の削除を行う
        """
        
        new_contours:list = []
        for i in range(0, len(contours)):
            # 小さな輪郭は削除する
            if len(contours[i]) > 0:                
                if cv2.contourArea(contours[i]) > 400:
                    new_contours.append(contours[i])

        # 一番外側の輪郭は省く
        new_contours = new_contours[1:]

        # 枠線の外側の輪郭のみに絞
        dst: list = []
        for i in range(len(new_contours)):
            if i % 2 == 0:
                dst.append(new_contours[i])

        return dst

    def exists_point(self, contour, pt: Point) -> bool:
        """
        引数のヒット座標が輪郭の内側に存在するか調べる
        """
        ret = cv2.pointPolygonTest(contour, pt.point(), measureDist=False)
        return ret > 0

    def exists_point_n(self, contours:list, point_n: int, pt: Point) -> bool:
        """
            引数のヒット座標がpoint_n点かどうか調べる
            (例: point_n = 4) ポイント4の内側に存在するかつ、ポイント5の内側には存在しない -> ポイントは4
            @input
                point_n     : 調べたいポイント
                pt          : ヒット座標
        """
        exists_a: bool = self.exists_point(
            contours[point_n - MIN_POINT], pt)

        # 最大ポイントの内側の場合、それより高い点は存在しないのでtrueを返す
        if point_n == MAX_POINT:
            if exists_a:
                return True
            else:
                return False

        exists_b: bool = self.exists_point(
            contours[point_n - MIN_POINT + 1], pt)

        return exists_a and (not exists_b)

    def detectHitInfo(self, image: cv2.Mat, pt_list: list[Point]) -> Tuple[list[TargetSiteHitPoint], cv2.Mat]:
        """
        ヒット情報を返す
        @input
            image   :   トリミングされた射撃後の画像
            pt_list :   射撃座標リスト

        @output
            list    :   ヒットポイント情報リスト
            cv2.Mat :   輪郭が塗られた画像
        """
        # グレースケール化
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 閾値処理
        _, thresh = cv2.threshold(image_gray, 95, 255, cv2.THRESH_BINARY)

        # 輪郭検出 （cv2.RETER_TREE）
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 小さい輪郭を削除して文字を消す
        contours = self.removeUnuseContours(contours)

        # 輪郭が7個でない場合、エラーをはく
        if not len(contours) == CONTOURS_COUNT:
            raise Exception(f"輪郭の個数が{len(contours)}個です。{CONTOURS_COUNT}個になるように画像の取り直しが必要です。")

        img1 = cv2.drawContours(image, contours, -1,
                             (0, 255, 0), 2, cv2.LINE_AA)        

        # ヒットポイントの取得
        dst: list[TargetSiteHitPoint] = []
        for pt in pt_list:
            for point_n in reversed(range(MIN_POINT, MAX_POINT + 1)):
                exists: bool = self.exists_point_n(contours, point_n, pt)
                if exists:                    
                    dst.append(TargetSiteHitPoint(self.site_id, pt, point_n))                    
        
        return dst, img1

    def drawHitPoint(self, image: cv2.Mat, ht_list: list[TargetSiteHitPoint]) -> cv2.Mat:
        """
            点数と座標の記載
        """        
        for ht in ht_list:
            cv2.circle(image, center=ht.pt.point(), radius=5, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_4, shift=0)
            cv2.putText(image,
                text=f"(x={ht.pt.x}, y={ht.pt.y} hit point={ht.hit_point})",
                org=(ht.pt.x + 10, ht.pt.y + 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=1,
                lineType=cv2.LINE_4)

        return image