from entities.BaseResponse import BaseResponse

from entities.SiteCommand import SiteCommand

class FetchSiteCommandResponse(BaseResponse):
    """
    fetch_site_command APIのレスポンス
    """
    def __init__(self, return_code: int, message: str, site_command:SiteCommand) -> None:
        super().__init__(return_code, message)
        self.site_command = site_command