class BaseResponse(object):
    """
    APIが返すレスポンス
    """

    def __init__(self, return_code:int, message:str) -> None:
        """
        @params
            return_code : 0:正常, 1:異常
            message     : メッセージ
        """
        self.return_code = return_code
        self.message = message