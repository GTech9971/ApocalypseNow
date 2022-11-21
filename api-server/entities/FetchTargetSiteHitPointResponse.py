from __future__ import annotations

from entities.BaseResponse import BaseResponse
from entities.TargetSiteHitPoint import TargetSiteHitPoint


class FetchTargetSiteHitPoint(BaseResponse):
    """
    fetch_target_site_hit_point APIのレスポンス
    """

    def __init__(self, return_code: int, message: str, ht_list: list[TargetSiteHitPoint]) -> None:
        super().__init__(return_code, message)
        self.ht_list = ht_list
