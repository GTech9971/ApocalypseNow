from services.ap2n.DbConnector import DbConnector


class TargetSiteDbService(DbConnector):

    def __init__(self) -> None:
        super().__init__()

    def publishSiteId(self) -> int:
        """
        ターゲットサイトの新しいidを採番する
        """

        con = self.connect()
        cursor = con.cursor()

        sql = "SELECT MAX(id) FROM target_sites;"
        cursor.execute(sql)

        rows = cursor.fetchall()
        for row in rows:
            print(row)
