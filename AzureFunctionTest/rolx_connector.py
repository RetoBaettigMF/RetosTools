import mysql.connector
import pandas as pd
import os

USERQUERY ="""
SELECT u.FirstName, u.LastName, u.Email, ups.Factor
FROM users u
JOIN userparttimesettings ups ON u.Id = ups.UserId
WHERE (ups.UserId, ups.StartDate) IN (
    SELECT UserId, MAX(StartDate)
    FROM userparttimesettings
    GROUP BY UserId
)
"""
class rolX:
    __cursor = None

    def __init__(self):
        password = os.getenv('ROLX_PASSWORD')
        if password is None:
            print("Please set ROLX_PASSWORD environment variable.")
            return
        self.__mydb = mysql.connector.connect(
            host="rolx-database.mariadb.database.azure.com",
            user="rolx_prod_readonly@rolx-database",
            password=password,
            database="rolx_production"
        )
        self.__cursor = self.__mydb.cursor()

    def __del__(self):
        if self.__mydb is not None:
            self.__mydb.close()

    def get_users(self):
        self.__cursor.execute(USERQUERY)
        df = pd.DataFrame(self.__cursor.fetchall(), columns=self.__cursor.column_names)
        return df
    
