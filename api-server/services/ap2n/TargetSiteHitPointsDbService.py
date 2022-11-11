import MySQLdb

from services.ap2n.DbConnector import DbConnector

from entities.TargetSiteHitPoint import TargetSiteHitPoint


class TargetSiteHitPointsDbService(DbConnector):
    """
    target_site_hit_pointsテーブルの操作を行う
    """

    def __init__(self) -> None:
        super().__init__()

    def record(self, hit_point_list: list):
        """
        ターゲットサイトヒットポイントをdbに追加する
        """
        try:
            con = self.connect()
            cursor: MySQLdb.cursors.Cursor = con.cursor()

            # TODO データがかぶるため、古いデータを一旦削除する
            sql = f"DELETE FROM target_site_hit_points WHERE target_site_id = {hit_point_list[0].site_id}"
            cursor.execute(sql)

            sql = ""
            for hit_point in hit_point_list:
                sql += f"INSERT INTO target_site_hit_points VALUES({hit_point.site_id}, {hit_point.pt.x}, {hit_point.pt.y}, {hit_point.hit_point}, NOW());"

            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()
        except Exception as e:
            raise e
        pass