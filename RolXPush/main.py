import mysql.connector
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

def get_table_info(db, table):
    headers=get_headers(db, table)
    result = "Table: " + table + "\n"
    for x in headers:
        result += "   Field: "+x[0] + ":" + x[1] + "\n"
    print(result)
    return result

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
    tables = get_tables(mydb)
    for table in tables:
        get_table_info(mydb, table)
    
    mydb.close()

if __name__ == "__main__":
    main()