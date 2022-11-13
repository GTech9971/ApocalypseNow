from entities.BaseResponse import BaseResponse

class ShootTargetSiteResponse(BaseResponse):
    """
    射撃後の画像アップロードAPIのレスポンス
    """

    def __init__(self, return_code: int, message: str, site_id:int, hit_point_list:list) -> None:
        """
        @params
            site_id         :   サイトid
            hit_point_list  :   ヒットポイント情報リスト
        """
        super().__init__(return_code, message)
        self.site_id = site_id
        self.hit_point_list = list