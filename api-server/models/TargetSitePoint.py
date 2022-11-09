import cv2

from HitPoint import HitPoint

# 最大ポイント
MAX_POINT: int = 10
# 最小ポイント
MIN_POINT: int = 4


class TargetSitePoint(object):
    """
    ターゲットサイトのヒット情報を管理する
    """

    def __init__(self, site_id: int, contours: list) -> None:
        self.site_id = site_id
        self.contours = contours
        self.hit_point_list: list[HitPoint] = []

    def append_hit_point(self, pt: HitPoint):
        """
        ヒットポイントをリス尾に追加する
        """
        self.hit_point_list.append(pt)

    def print_point_list(self):
        """
        ヒットポイントリストのポイントを表示させる
        """
        print(f"TargetSite Hit point info id:={self.site_id}")

        for pt in self.hit_point_list:
            for point_n in reversed(range(MIN_POINT, MAX_POINT + 1)):
                result: bool = self.exists_point_n(point_n, pt)
                if result:
                    print(f"(x={pt.x}, y={pt.y} point={point_n})")
                    continue

        print("done.")

    def exists_point(self, contour, pt: HitPoint) -> bool:
        """
        引数のヒット座標が輪郭の内側に存在するか調べる
        """
        ret = cv2.pointPolygonTest(contour, pt.point(), measureDist=False)

        return ret > 0

    def exists_point_n(self, point_n: int, pt: HitPoint) -> bool:
        """
            引数のヒット座標がpoint_n点かどうか調べる
            (例: point_n = 4) ポイント4の内側に存在するかつ、ポイント5の内側には存在しない -> ポイントは4
            @input
                point_n     : 調べたいポイント
                pt          : ヒット座標
        """
        exists_a: bool = self.exists_point(
            self.contours[point_n - MIN_POINT], pt)

        # 最大ポイントの内側の場合、それより高い点は存在しないのでtrueを返す
        if point_n == MAX_POINT:
            if exists_a:
                return True
            else:
                return False

            
        exists_b: bool = self.exists_point(
            self.contours[point_n - MIN_POINT + 1], pt)

        return exists_a and (not exists_b)
