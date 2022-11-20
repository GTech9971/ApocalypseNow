from __future__ import annotations

from entities.BaseResponse import BaseResponse

from entities.SiteCommand import SiteCommand

class FetchSiteCommandResponse(BaseResponse):
    """
    fetch_site_command APIのレスポンス
    """
    def __init__(self, return_code: int, message: str, command_list:list[SiteCommand]) -> None:
        super().__init__(return_code, message)
        self.command_list = command_list