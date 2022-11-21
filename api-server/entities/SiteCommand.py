class SiteCommand(object):
    """
    ビュワーからのコマンド情報
    """
    def __init__(self, id:int, site_id:int, command_id:int) -> None:
        """
        @params
            id          : サイトコマンドのid
            site_id     : サイトのid
            command_id  : コマンドのid
        """
        self.id = id
        self.site_id = site_id
        self.command_id = command_id
        self.created_at = None
        self.is_done = False