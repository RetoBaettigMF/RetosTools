from rolx_connector import rolX
from pandasql import sqldf

QUERY_VERRECHENBAR = """
 SELECT FirstName as Vorname, LastName as Nachname, SUM(Duration) as Total, 
 SUM(CASE WHEN ActivityIsBillable = TRUE THEN Duration ELSE 0 END) as Verrechenbar, 
 (SUM(CASE WHEN ActivityIsBillable = TRUE THEN Duration ELSE 0 END) / SUM(Duration)) * 100 as Verrechenbarkeit 
 FROM data GROUP BY FirstName, LastName ORDER BY Verrechenbarkeit DESC
 """

def main():
    rolx = rolX()
    data = rolx.get_last_num_days(10)
    result = sqldf(QUERY_VERRECHENBAR, locals())
    print(result)
    
        
if __name__ == "__main__":
    main()