class TargetSite(object):
    """
    的の情報を格納する
    """

    def __init__(self, id: int = -1, img_path: str = None, created_at: str = None) -> None:
        self.id = id
        self.img_path = img_path
        self.created_at = created_at
