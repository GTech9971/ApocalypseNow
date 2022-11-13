from entities.BaseResponse import BaseResponse
from entities.TargetSite import TargetSite

class UploadOriginalTargetSiteResponse(BaseResponse):
    """
    射撃前のターゲットサイトアップロードのレスポンス
    """

    def __init__(self, return_code: int, message: str, target_site:TargetSite) -> None:
        """
        @params
            target_site :   サイトの情報
        """
        super().__init__(return_code, message)
        self.target_site = target_site
        
