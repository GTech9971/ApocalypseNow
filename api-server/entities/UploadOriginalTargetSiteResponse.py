from entities.BaseResponse import BaseResponse

class UploadOriginalTargetSiteResponse(BaseResponse):
    """
    射撃前のターゲットサイトアップロードのレスポンス
    """

    def __init__(self, return_code: int, message: str, site_id:int, trim_rect:tuple) -> None:
        """
        @params
            site_id     : ターゲットサイトのid
            trim_rect   : トリミング座標(x,y,w,h)
        """
        super().__init__(return_code, message)
        self.site_id = site_id
        self.trim_rect = trim_rect
