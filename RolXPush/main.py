from rolx_connector import rolX
import argparse
from pandasql import sqldf
from teams_push import send_teams_message
from employees import employees, BUs

QUERY_VERRECHENBAR = """
 SELECT d.FirstName as Vorname, d.LastName as Nachname, SUM(Duration) as Total, 
 SUM(CASE WHEN ActivityIsBillable = TRUE THEN Duration ELSE 0 END) as Verrechenbar, 
 COALESCE(u.Factor*100, 100) as Anstellungsgrad, 
 (SUM(CASE WHEN ActivityIsBillable = TRUE THEN Duration ELSE 0 END) / SUM(Duration)) * 100 as Verrechenbarkeit, 
 (SUM(Duration) / COALESCE(u.Factor, 1) / 42 * 100) as Stundenbuchungsgrad
 FROM data d 
 LEFT JOIN users u ON d.FirstName = u.FirstName AND d.LastName = u.LastName
 GROUP BY d.FirstName, d.LastName ORDER BY d.LastName ASC
 """

def add_bu(df):
    # Eine neue Spalte "BU" zur Tabelle hinzufügen
    df['BU'] = ''

    # Die BU-Werte aus der Liste in die neue Spalte eintragen
    for i, row in df.iterrows():
        name = row['Nachname']
        vorname = row['Vorname']
        for employee in employees:
            if employee['Name'] == name and employee['Vorname'] == vorname:
                df.at[i, 'BU'] = employee['BU']
                break
    df= df.sort_values(by=['BU', 'Nachname'])
    return df

def add_leave(df, leave):
    # Eine neue Spalte "PaidLeave" zur Tabelle hinzufügen
    df['PaidLeave'] = ''

    # Die BU-Werte aus der Liste in die neue Spalte eintragen
    for i, row in df.iterrows():
        name = row['Nachname']
        vorname = row['Vorname']
        for j, leaveentry in leave.iterrows():
            if leaveentry['LastName'] == name and leaveentry['FirstName'] == vorname:
                df.at[i, 'PaidLeave'] = "TRUE"
                break
    return df

def get_billability(data, users, leave):
    result = sqldf(QUERY_VERRECHENBAR, locals())
    result = add_bu(result)
    result = add_leave(result, leave)
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

def format_billabilities_and_get_html(billability):
    df = billability

    def billability_map(value):
        if value < 50:
            return 'background-color: orange'
        elif value < 80:
            return 'background-color: yellow'
        else:
            return 'background-color: lightgreen'

    def booking_map(value):
        if value < 80:
            return 'background-color: orange'
        else:
            return 'background-color: lightgreen'

    styled_df = df.style.apply(lambda x: [''] * len(x), axis=1).applymap(billability_map, subset=['Verrechenbarkeit']).applymap(booking_map, subset=['Stundenbuchungsgrad'])
    html = styled_df.to_html(index=False)
    with open('output.html', 'w') as file:
        file.write(html)
    return html

def get_billabilties_per_bu(billability):
    # Get an array of billabilities per BU
    billabilities = []
    #for bu in billability['BU'].unique():
    for bu in BUs:
        part = billability[billability['BU'] == bu].copy()
        print(part.to_string())
        billabilities.append(part)
    return billabilities

def generate_statistics(data, users, leave):
    args = handle_arguments()
    billability = get_billability(data, users, leave)
    billabilities = get_billabilties_per_bu(billability)
    notbooked = sqldf("SELECT * FROM billability WHERE (Stundenbuchungsgrad < 80)", locals())
    
    if args.sendteams:
        for bu, df in billabilities:
            send_teams_message(bu.iloc[0]['BU']+": Verrechenbarkeit in den letzten 7 Tagen:", format_billabilities_and_get_html(df))
        send_teams_message("Diese User haben ev. bezahlte Abwesenheiten gehabt oder noch nicht alles gebucht:", notbooked.to_html(index=False))
    else:
        for bu in billabilities:
            print(bu.iloc[0]['BU']+": Verrechenbarkeit in den letzten 7 Tagen:\n", bu.to_string())
        print("\nDiese User haben ev. bezahlte Abwesenheiten gehabt oder noch nicht alles gebucht:\n")
        print(notbooked.to_string())

def main():
    rolx = rolX()
    data = rolx.get_last_num_days(7)
    data.to_excel('output.xlsx', index=False)
    users = rolx.get_users()
    leave = rolx.get_last_num_days_levae(7)
    generate_statistics(data, users, leave)
    
    
        
if __name__ == "__main__":
    main()