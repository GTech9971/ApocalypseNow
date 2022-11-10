from entities.Point import Point


class TargetSiteHitPoint(object):
    """
    的のヒットした情報を格納する
    """

    def __init__(self, site_id: int, pt: Point, hit_point: int, created_at: str) -> None:
        self.site_id = site_id
        self.pt = pt
        self.hit_point = hit_point
        self.created_at = created_at
