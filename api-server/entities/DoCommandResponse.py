from entities.BaseResponse import BaseResponse


class DoCommandResponse(BaseResponse):
    """
    コマンド実行APIのレスポンス
    """

    def __init__(self, return_code: int, message: str, site_command_id:int) -> None:
        super().__init__(return_code, message)
        self.site_command_id = site_command_id