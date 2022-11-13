class TargetSite(object):
    """
    的の情報を格納する
    """

    def __init__(self, site_id: int, img_path: str, trim_rect:tuple) -> None:
        """
            @param
                id          :   サイトのid
                img_path    :   トリミング＆リサイズ後の画像保存先パス
                trim_rect   :   トリミング時の座標(x,y,w,h)                
        """

        self.site_id = site_id
        self.img_path = img_path        
        self.trim_x = trim_rect[0]
        self.trim_y = trim_rect[1]
        self.trim_w = trim_rect[2]
        self.trim_h = trim_rect[3]
        self.created_at = None
        self.hit_img_path = None
        self.updated_at = None
    

    def getTrimRect(self)->tuple:
        """
        トリミング座標を返す(x,y,w,h)
        """
        return (self.trim_x, self.trim_y,self.trim_w,self.trim_h)
