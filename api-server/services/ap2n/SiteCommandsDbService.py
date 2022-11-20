from __future__ import annotations

import MySQLdb
import MySQLdb.cursors

from services.ap2n.DbConnector import DbConnector

from entities.SiteCommand import SiteCommand

class SiteCommandsDbService(DbConnector):
    """
    site_commandsテーブルの操作を行う
    """
    def __init__(self) -> None:
        super().__init__()
    
    def doCommand(self, site_command:SiteCommand):
        """
        ビュワーのコマンドを記録する
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"INSERT INTO site_commands(target_site_id, command_id, created_at) VALUES({site_command.site_id}, {site_command.command_id}, NOW());"
        cursor.execute(sql)
        con.commit()

        cursor.close()
        con.close()
        
    def fetchCommand(self, site_id:int) -> list[SiteCommand]:
        """
        ビュワーからのコマンドを取得する
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"SELECT id, target_site_id, command_id, created_at FROM site_commands WHERE target_site_id = {site_id};"
        cursor.execute(sql)                    

        rows = cursor.fetchall()

        cursor.close()
        con.close()

        command_list:list[SiteCommand] = []
        for row in rows:
            if row[0] is None:
                return []
            id, target_site_id, command_id, created_at = row
            site_command = SiteCommand(id, target_site_id, command_id)
            site_command.created_at = created_at

            command_list.append(site_command)
            
        return command_list
    
    def doneCommand(self, site_command_id:int):
        """
            コマンドの完了処理を行う
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"DELETE FROM site_commands WHERE id = {site_command_id}"
        cursor.execute(sql)
        con.commit()

        cursor.close()
        con.close()