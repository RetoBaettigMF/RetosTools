from rolx_connector import rolX
import argparse
from pandasql import sqldf
from teams_push import send_teams_message

QUERY_VERRECHENBAR = """
 SELECT d.FirstName as Vorname, d.LastName as Nachname, SUM(Duration) as Total, 
 SUM(CASE WHEN ActivityIsBillable = TRUE THEN Duration ELSE 0 END) as Verrechenbar, 
 (SUM(CASE WHEN ActivityIsBillable = TRUE THEN Duration ELSE 0 END) / SUM(Duration)) * 100 as Verrechenbarkeit, 
 COALESCE(u.Factor*100, 100) as Anstellungsgrad, (SUM(Duration) / COALESCE(u.Factor, 1) / 42 * 100) as Stundenbuchungsgrad
 FROM data d 
 LEFT JOIN users u ON d.FirstName = u.FirstName AND d.LastName = u.LastName
 GROUP BY d.FirstName, d.LastName ORDER BY Verrechenbarkeit DESC
 """


def get_billability(data, users):
    result = sqldf(QUERY_VERRECHENBAR, locals())
    result["Total"] = result["Total"].astype(int)
    result["Verrechenbar"] = result["Verrechenbar"].astype(int)
    result["Verrechenbarkeit"] = result["Verrechenbarkeit"].astype(int)
    result["Anstellungsgrad"] = result["Anstellungsgrad"].astype(int)
    result["Stundenbuchungsgrad"] = result["Stundenbuchungsgrad"].astype(int)
    
    print(result.to_string())
    return result

def handle_arguments():
    parser = argparse.ArgumentParser(description='Generate statistics for rolX')
    parser.add_argument('--sendteams', action='store_true',
                        help='sends the statistics to the teams channel')
    return parser.parse_args()

def generate_statistics(data, users):
    args = handle_arguments()
    billability = get_billability(data, users)
    notbooked = sqldf("SELECT * FROM billability WHERE (Stundenbuchungsgrad < 80)", locals())
    if args.sendteams:
        send_teams_message("Verrechenbarkeit in den letzten 7 Tagen:", billability.to_html(index=False))
        send_teams_message("Diese User haben wahrscheinlich noch nicht alles gebucht:", notbooked.to_html(index=False))
    else:
        print(billability.to_string())
        print(notbooked.to_string())

def main():
    rolx = rolX()
    data = rolx.get_last_num_days(7)
    data.to_excel('output.xlsx', index=False)
    users = rolx.get_users()
    generate_statistics(data, users)
    
    
        
if __name__ == "__main__":
    main()