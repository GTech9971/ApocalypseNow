from __future__ import annotations
import MySQLdb

from services.ap2n.DbConnector import DbConnector

from entities.TargetSiteHitPoint import TargetSiteHitPoint
from entities.Point import Point


class TargetSiteHitPointsDbService(DbConnector):
    """
    target_site_hit_pointsテーブルの操作を行う
    """

    def __init__(self) -> None:
        super().__init__()

    def record(self, hit_point_list: list[TargetSiteHitPoint]):
        """
        ターゲットサイトヒットポイントをdbに追加する
        """
        try:
            con = self.connect()
            cursor: MySQLdb.cursors.Cursor = con.cursor()

            # TODO データがかぶるため、古いデータを一旦削除する
            sql = f"DELETE FROM target_site_hit_points WHERE target_site_id = {hit_point_list[0].site_id}"
            cursor.execute(sql)

            sql = "INSERT INTO target_site_hit_points(target_site_id, x, y, hit_point, created_at) VALUES\n"
            for hit_point in hit_point_list:
                sql += f"   ({hit_point.site_id}, {hit_point.pt.x}, {hit_point.pt.y}, {hit_point.hit_point}, NOW()),\n"

            sql = sql[0:len(sql) - 2] + ";"

            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()
        except Exception as e:
            raise e

    def fetchHitPoints(self, site_id: int) -> list[TargetSiteHitPoint]:
        """
        site_idに一致するヒットポインと情報を返す
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"SELECT target_site_id, x, y, hit_point, created_at FROM target_site_hit_point WHERE target_site_id = {site_id};"
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        con.close()

        ht_list: list[TargetSiteHitPoint] = []
        for row in rows:
            if row[0] is None:
                return []

            target_site_id, x, y, hit_point, created_at = row

            ht: TargetSiteHitPoint = TargetSiteHitPoint(
                site_id=target_site_id, pt=Point(x=x, y=y), hit_point=hit_point)
            ht.created_at = created_at
            ht_list.append(ht)

        return ht_list
