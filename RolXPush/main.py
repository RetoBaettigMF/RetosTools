from rolx_connector import rolX
from pandasql import sqldf
from teams_push import send_teams_message

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
    print(result.to_string())
    send_teams_message("Verrechenbarkeit in den letzten 7 Tagen:", result.to_html(index=False))
    
        
if __name__ == "__main__":
    main()