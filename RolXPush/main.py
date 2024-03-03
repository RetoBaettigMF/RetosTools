import mysql.connector
import pandas as pd
import os

def get_tables(db):
    mycursor = db.cursor()
    mycursor.execute("SHOW TABLES")
    results = mycursor.fetchall()
    string_list = [item[0] for item in results]
    return string_list

def get_users(db):
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM users")
    results = mycursor.fetchall()
    return results

def get_activities(db, num):
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM activities LIMIT " + str(num))
    results = mycursor.fetchall()
    return mycursor

def get_headers(db, table):
    mycursor = db.cursor()
    mycursor.execute("SHOW COLUMNS FROM " + table)
    results = mycursor.fetchall()
    return results

def get_month(db, year, month):
    mycursor = db.cursor()
    datestart = str(year) + '-' + str(month) + '-1'
    dateend =str(year) + '-' + str(month) + '-31'
    where = "WHERE r.Date >= '" + datestart + "' AND r.Date <= '" + dateend + "'"

    query = """
SELECT r.Date, u.Email, sp.Projectnumber, sp.Number AS Subprojectnumber, a.Number AS ActivityNumber, 
    CONCAT('#', LPAD(sp.ProjectNumber, 4, '0'), '.', LPAD(sp.Number, 3, '0')) AS OrderNumber,
    sp.CustomerName AS Customer, sp.ProjectName AS Project, sp.Name AS Subproject, 
    a.Name AS Activity, (re.DurationSeconds - COALESCE(re.PauseSeconds, 0)) AS Duration, 
    b.Name AS Billability, re.Comment
FROM recordentries re
JOIN activities a ON re.ActivityId = a.Id
JOIN subprojects sp ON a.SubprojectId = sp.Id
JOIN records r ON re.RecordId = r.Id
JOIN users u ON r.UserId = u.Id
JOIN billabilities b ON a.BillabilityId = b.Id
"""
    query += where
    mycursor.execute(query)
    df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
    return df

def get_table_info(db, table):
    headers=get_headers(db, table)
    result = "## Table: " + table + "\n"
    result += "| Field | Type     |\n"
    result += "|-------|----------|\n"
    for x in headers:
        result += "| "+x[0] + " | " + x[1] + "|\n"
    print(result)
    return result

def print_database_schema(db):
    tables = get_tables(db)
    for table in tables:
        get_table_info(db, table)

def main():
    password = os.getenv('ROLX_PASSWORD')
    if password is None:
        print("Please set ROLX_PASSWORD environment variable.")
        return
    mydb = mysql.connector.connect(
        host="rolx-database.mariadb.database.azure.com",
        user="rolx_prod@rolx-database",
        password=password,
        database="rolx_production"
    )

    #print_database_schema(mydb)
    
    df = get_month(mydb, 2024, 2)
    print(df.head().to_string())
    df.to_excel('output.xlsx', index=False)
    
    mydb.close()

if __name__ == "__main__":
    main()