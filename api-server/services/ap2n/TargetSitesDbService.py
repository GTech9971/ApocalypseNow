from __future__ import annotations

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

    def fetchAllTargetSite(self)->list[TargetSite]:
        """
        すべてのtarget_siteを返す
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = "SELECT id, img_path, hit_img_path, created_at, updated_at, trim_x, trim_y, trim_w, trim_h  FROM target_sites;"
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        con.close()

        site_list:list[TargetSite] = []
        for row in rows:
            if row[0] is None:
                return []
            
            site_id, img_path, hit_img_path, created_at, updated_at, trim_x, trim_y, trim_w, trim_h = row
            target_site:TargetSite = TargetSite(site_id=int(site_id), img_path=img_path, trim_rect=(int(trim_x), int(trim_y), int(trim_w), int(trim_h)))
            target_site.created_at = created_at
            target_site.hit_img_path = hit_img_path
            target_site.updated_at = updated_at
            
            site_list.append(target_site)
        
        return site_list
            


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
            
            return int(row[0]) + 1

    
    def fetchTargetSite(self, site_id:int)->TargetSite:
        """
            引数のサイトidからサイト情報を返す
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"SELECT id, img_path, hit_img_path, created_at, updated_at, trim_x, trim_y, trim_w, trim_h FROM target_sites WHERE id = {site_id};"
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        con.close()

        for row in rows:
            if row[0] is None:
                return None
            
            id, img_path, hit_img_path, created_at, updated_at, trim_x, trim_y, trim_w, trim_h = row

            result: TargetSite = TargetSite(site_id==id, img_path=img_path, trim_rect=(int(trim_x), int(trim_y), int(trim_w), int(trim_h)))
            result.created_at = created_at
            result.updated_at = updated_at
            result.hit_img_path = hit_img_path
            return result


    def record(self, target_site: TargetSite):
        """
        ターゲットサイトをdbに追加する(新規)
        @input
            target_site :   dbに登録する
        """
        try:
            con = self.connect()
            cursor: MySQLdb.cursors.Cursor = con.cursor()

            
            sql = f"""INSERT INTO target_sites(id, img_path, trim_x, trim_y, trim_w, trim_h, created_at) 
                        VALUES({target_site.site_id}, '{target_site.img_path}', {target_site.trim_x}, {target_site.trim_y}, {target_site.trim_w}, {target_site.trim_h}, NOW());"""
            
            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()
        except Exception as e:
            raise e
    
    
    def recordHitImagePath(self, site_id:int, hit_img_path:str):
        """
        ヒット後のサイト画像パスをsite_idと一致するレコードに記録する(更新)
        @input
            site_id     :   サイトid
            hit_img_path:   ヒット後の画像の保存先パス
        """

        try:
            con = self.connect()
            cursor: MySQLdb.cursors.Cursor = con.cursor()

            sql = f"""UPDATE target_sites SET hit_img_path = '{hit_img_path}', updated_at = NOW() WHERE id = {site_id};"""                        
            
            cursor.execute(sql)
            con.commit()

            cursor.close()
            con.close()
        except Exception as e:
            raise e
