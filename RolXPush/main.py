import mysql.connector
import pandas as pd
import os
from rolx_connector import rolX

def main():
    rolx = rolX()
    schema = rolx.get_database_schema()
    print(schema)
    
    df = rolx.get_last_num_days(10)
    print(df.head().to_string())
    df.to_excel('output.xlsx', index=False)
        
if __name__ == "__main__":
    main()