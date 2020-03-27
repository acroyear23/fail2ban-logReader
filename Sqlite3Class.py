import sqlite3


# DATABASE CREATION - fail2ban.db in working directory
# Columns:
# HOST, DATE, TIME, MESSAGE, SERVICE, BAN_STATUS, IP

class Sqlite3:
    def __init__(self):
        self.sql_conn = sqlite3.connect("fail2ban.db")
        self.cursor = self.sql_conn.cursor()
        # CREATES TABLE if Fail2Ban.IP.db does not exist
        # Uses UNIQUE to maintain DB and add new files
        # id INTEGER PRIMARY KEY adds numbering of entries
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS fail2ban_table"
            " (id INTEGER PRIMARY KEY, host, date TEXT, time TEXT, message TEXT,"
            " service TEST, ban_status TEXT, ip TEXT,UNIQUE(date,time,ban_status))")

        self.sql_conn.commit()
        self.sql_conn.close()

    def insert_db(self, temp_file):
        for line in temp_file:
            self.sql_conn = sqlite3.connect('fail2ban.db')
            self.cursor = self.sql_conn.cursor()
            host, date, time, message, service, ban_status, ip = line.split(",")
            # Uses INSERT OR IGNORE to work with UNIQUE in above table creation
            self.cursor.execute(" INSERT OR IGNORE INTO fail2ban_table "
                                "(host, date,time,message,service,ban_status,ip) VALUES(?,?,?,?,?,?,?)",
                                (host, date, time, message, service, ban_status, ip))
            self.sql_conn.commit()
            self.sql_conn.close()

    def view_db(self):
        self.sql_conn = sqlite3.connect('fail2ban.db')
        self.cursor = self.sql_conn.cursor()
        self.cursor.execute("SELECT * FROM fail2ban_table")
        rows = self.cursor.fetchall()
        self.sql_conn.commit()
        self.sql_conn.close()
        return rows

    def view_sort(self, sort):
        self.sql_conn = sqlite3.connect('fail2ban.db')
        self.cursor = self.sql_conn.cursor()
        self.cursor.execute(sort)
        rows = self.cursor.fetchall()
        self.sql_conn.commit()
        self.sql_conn.close()
        return rows
