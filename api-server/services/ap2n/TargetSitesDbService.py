import MySQLdb
import MySQLdb.cursors

from services.ap2n.DbConnector import DbConnector

from entities.TargetSite import TargetSite


class TargetSitesDbService(DbConnector):
    """
    target_sites テーブルに関する操作を行う
    """

    def __init__(self) -> None:
        super().__init__()

    def publishSiteId(self) -> int:
        """
        ターゲットサイトの新しいidを採番する
        """

        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = "SELECT MAX(id) FROM target_sites;"
        cursor.execute(sql)

        rows = cursor.fetchall()

        cursor.close()
        con.close()

        for row in rows:
            if row[0] is None:
                return 1
            else:
                return int(row[0]) + 1

    def record(self, target_site: TargetSite, is_new: bool):
        """
        ターゲットサイトをdbに追加する(新規) or 画像を更新する
        """
        try:
            con = self.connect()
            cursor: MySQLdb.cursors.Cursor = con.cursor()

            # 新規の場合
            if is_new:
                sql = f"INSERT INTO target_sites VALUES({target_site.id}, '{target_site.img_path}', NOW());"
            else:  # 更新の場合、画像パスのみを更新する
                sql = f"UPDATE target_sites SET img_path ='{target_site.img_path}' WHERE id = {target_site.id});"

            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()
        except Exception as e:
            raise e
