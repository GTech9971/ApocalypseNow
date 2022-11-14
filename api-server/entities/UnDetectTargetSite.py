class UnDetectTargetSite(object):
    """
    yoloで検出できなかった画像の情報
    """

    def __init__(self, id:int = None, img_path:str ="") -> None:
        """
        @param
            id          :   未検出画像id
            img_path    :   未検出画像保存先パス        
        """
        self.id = id
        self.img_path = img_path
        self.created_at = None