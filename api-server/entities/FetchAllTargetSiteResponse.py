from entities.BaseResponse import BaseResponse

class FetchAllTargetSieResponse(BaseResponse):
    """
    すべてのサイトを返すAPIのレスポンス
    """

    def __init__(self, return_code: int, message: str, target_site_list:list) -> None:
        """
        @params
            target_site_list    :   ターゲットサイト情報のリスト
        """
        super().__init__(return_code, message)
        self.target_site_list = target_site_list
