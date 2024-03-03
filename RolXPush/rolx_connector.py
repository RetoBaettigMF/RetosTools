import mysql.connector
import pandas as pd
import os

BASEQUERY = """
SELECT r.Date, u.FirstName, u.LastName, sp.Projectnumber, sp.Number AS Subprojectnumber, a.Number AS ActivityNumber, 
    CONCAT('#', LPAD(sp.ProjectNumber, 4, '0'), '.', LPAD(sp.Number, 3, '0')) AS OrderNumber,
    sp.CustomerName AS Customer, sp.ProjectName AS Project, sp.Name AS Subproject, 
    a.Name AS Activity, ((re.DurationSeconds - COALESCE(re.PauseSeconds, 0)) / 3600) AS Duration, 
    b.Name AS Billability, b.IsBillable as ActivityIsBillable, re.Comment
FROM recordentries re
JOIN activities a ON re.ActivityId = a.Id
JOIN subprojects sp ON a.SubprojectId = sp.Id
JOIN records r ON re.RecordId = r.Id
JOIN users u ON r.UserId = u.Id
JOIN billabilities b ON a.BillabilityId = b.Id
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
            user="rolx_prod@rolx-database",
            password=password,
            database="rolx_production"
        )
        self.__cursor = self.__mydb.cursor()

    def __del__(self):
        if self.__mydb is not None:
            self.__mydb.close()

    def __query(self, query):
        self.__cursor.execute(query)
        df = pd.DataFrame(self.__cursor.fetchall(), columns=self.__cursor.column_names)
        df['Duration'] = df['Duration'].astype(float)
        df['ActivityIsBillable'] = df['ActivityIsBillable'].astype(bool)
        return df

    def get_users(self):
        df = self.__query("SELECT * FROM users")
        return df
    
    def get_tables(self):
        self.__cursor.execute("SHOW TABLES")
        results = self.__cursor.fetchall()
        string_list = [item[0] for item in results]
        return string_list

    def get_headers(self, table):
        self.__cursor.execute("SHOW COLUMNS FROM " + table)
        results = self.__cursor.fetchall()
        return results

    def get_table_info(self, table):
        headers=self.get_headers(table)
        result = "## Table: " + table + "\n"
        result += "| Field | Type     |\n"
        result += "|-------|----------|\n"
        for x in headers:
            result += "| "+x[0] + " | " + x[1] + "|\n"
        print(result)
        return result

    def get_database_schema(self):
        tables = self.get_tables()
        for table in tables:
            self.get_table_info(table)

    def get_month(self, year, month):
        datestart = str(year) + '-' + str(month) + '-1'
        dateend =str(year) + '-' + str(month) + '-31'
        where = "WHERE r.Date >= '" + datestart + "' AND r.Date <= '" + dateend + "'"
        query = BASEQUERY + where
        df = self.__query(query)
        return df

    def get_last_num_days(self, days):
        query = BASEQUERY + "WHERE r.Date >= DATE_SUB(CURDATE(), INTERVAL " + str(days) + " DAY)"
        df = self.__query(query)
        return df
    
