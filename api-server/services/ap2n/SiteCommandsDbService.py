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

        cursor.close()
        con.close()
        
    def fetchCommand(self, site_id:int) -> SiteCommand:
        """
        ビュワーからのコマンドを取得する
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"""SELECT target_site_id, command_id, created_at FROM site_commands WHERE target_site_id = {site_id} AND
                    created_at = (SELECT MAX(created_at) FROM site_commands WHERE target_site_id = {site_id});"""
        cursor.execute(sql)

        rows = cursor.fetchall()

        cursor.close()
        con.close()

        site_command:SiteCommand = None
        for row in rows:
            if row[0] is None:
                return None
            target_site_id, command_id, created_at = row
            site_command = SiteCommand(target_site_id, command_id)
            site_command.created_at = created_at
            
        return site_command
    
    def doneCommand(self, site_command:SiteCommand):
        """
            コマンドの完了処理を行う
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"""DELETE FROM site_commands WHERE = 
                target_site_id = {site_command.site_id} AND command_id = {site_command.command_id} AND created_at = {site_command.created_at};"""
        cursor.execute(sql)

        cursor.close()
        con.close()