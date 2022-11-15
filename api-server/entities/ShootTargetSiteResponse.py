from __future__ import annotations

from entities.BaseResponse import BaseResponse
from entities.TargetSiteHitPoint import TargetSiteHitPoint

class ShootTargetSiteResponse(BaseResponse):
    """
    射撃後の画像アップロードAPIのレスポンス
    """

    def __init__(self, return_code: int, message: str, site_id:int, hit_point_list:list[TargetSiteHitPoint]) -> None:
        """
        @params
            site_id         :   サイトid
            hit_point_list  :   ヒットポイント情報リスト
        """
        super().__init__(return_code, message)
        self.site_id = site_id
        self.hit_point_list = hit_point_list