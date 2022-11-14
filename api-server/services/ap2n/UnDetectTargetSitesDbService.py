import MySQLdb
import MySQLdb.cursors

from services.ap2n.DbConnector import DbConnector

from entities.UnDetectTargetSite import UnDetectTargetSite

class UnDetectTargetSitesDbService(DbConnector):
    """
    undetect_target_sitesテーブルに対する操作を行う
    """

    def __init__(self) -> None:
        super().__init__()

    
    def record(self, undetect_target_site: UnDetectTargetSite):
        """
        未検出ターゲットサイトをdbに追加する
        @input
            undetect_target_site :   dbに登録する未検出サイト情報
        """
        try:
            con = self.connect()
            cursor: MySQLdb.cursors.Cursor = con.cursor()
            
            sql = f"""INSERT INTO undetect_target_sites(img_path, created_at) 
                        VALUES('{undetect_target_site.img_path}', NOW());"""
            
            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()
        except Exception as e:
            raise e