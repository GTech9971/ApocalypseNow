class Command(object):
    """
    コマンドの情報
    """
    def __init__(self, id:int, command_desc:str) -> None:
        self.id = id
        self.command_desc = command_desc
        self.created_at = None