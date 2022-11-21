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

    def doCommand(self, site_command: SiteCommand) -> int:
        """
        ビュワーのコマンドを記録する
        サイトIDが未確定の場合は、site_id = -1で登録する
        @return
            新しく登録したサイトコマンドid
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql: str = ""
        # ターゲットサイト確定コマンドなどはサイトIDが決まっていない場合がある
        if site_command.site_id is None:
            sql = f"INSERT INTO site_commands(target_site_id, command_id, created_at) VALUES(-1, {site_command.command_id}, NOW());"
        else:
            sql = f"INSERT INTO site_commands(target_site_id, command_id, created_at) VALUES({site_command.site_id}, {site_command.command_id}, NOW());"

        cursor.execute(sql)
        con.commit()

        site_command_id: int = int(cursor.lastrowid)

        cursor.close()
        con.close()

        return site_command_id

    def fetchCommand(self, site_id: int) -> list[SiteCommand]:
        """
        ビュワーから未実行のコマンドを取得する
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()

        sql = f"SELECT id, target_site_id, command_id, created_at, is_done FROM site_commands WHERE target_site_id = {site_id} AND is_done = false;"
        cursor.execute(sql)

        rows = cursor.fetchall()

        cursor.close()
        con.close()

        command_list: list[SiteCommand] = []
        for row in rows:
            if row[0] is None:
                return []
            id, target_site_id, command_id, created_at, is_done = row
            site_command = SiteCommand(id, target_site_id, command_id)
            site_command.created_at = created_at
            site_command.is_done = is_done

            command_list.append(site_command)

        return command_list

    def doneCommand(self, site_command_id: int, site_id: int = None):
        """
            コマンドの完了処理を行う
            @params
                site_command_id : 終了するコマンドid
                site_id         : 更新するターゲットサイトID(*デフォルトはNone 値が指定された場合のみ更新する)
        """
        con = self.connect()
        cursor: MySQLdb.cursors.Cursor = con.cursor()
        sql: str = ""
        if site_id is None:
            sql = f"UPDATE site_commands SET is_done = true WHERE id = {site_command_id};"
        else:
            sql = f"UPDATE site_commands SET is_done = true, target_site_id = {site_id} WHERE id = {site_command_id};"

        cursor.execute(sql)
        con.commit()

        cursor.close()
        con.close()
