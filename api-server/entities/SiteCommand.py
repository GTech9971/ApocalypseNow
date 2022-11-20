class SiteCommand(object):
    """
    ビュワーからのコマンド情報
    """
    def __init__(self, site_id:int, command_id:int) -> None:
        self.site_id = site_id
        self.command_id = command_id
        self.created_at = None