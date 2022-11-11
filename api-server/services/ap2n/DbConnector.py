import MySQLdb


class DbConnector(object):

    def __init__(self) -> None:
        self.USER_NAME = "root"
        self.password = "rootpass"
        self.host = "localhost"
        self.db = "ap2n"

    def connect(self) -> MySQLdb.Connection:
        return MySQLdb.connect(user=self.USER_NAME, passwd=self.password, host=self.host, db=self.db)
