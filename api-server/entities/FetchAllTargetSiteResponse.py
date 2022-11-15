from __future__ import annotations

from entities.BaseResponse import BaseResponse
from entities.TargetSite import TargetSite

class FetchAllTargetSieResponse(BaseResponse):
    """
    すべてのサイトを返すAPIのレスポンス
    """

    def __init__(self, return_code: int, message: str, target_site_list:list[TargetSite]) -> None:
        """
        @params
            target_site_list    :   ターゲットサイト情報のリスト
        """
        super().__init__(return_code, message)
        self.target_site_list = target_site_list
