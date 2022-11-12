from entities.Point import Point


class TargetSiteHitPoint(object):
    """
    的のヒットした情報を格納する
    """

    def __init__(self, site_id: int, pt: Point, hit_point: int) -> None:
        """
        @param
            site_id     : サイトのid
            pt          : ヒットポイント座標
            hit_point   : ヒットポイントの点数
        """
        self.site_id = site_id
        self.pt = pt
        self.hit_point = hit_point
        self.created_at = None
