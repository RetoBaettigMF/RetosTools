import re
import sys
import datetime
import matplotlib.pyplot as plt
import datetime

def convert_timestamp_to_string(unix_timestamp):
    # Konvertieren Sie den Unix-Timestamp in ein datetime-Objekt
    dt_object = datetime.datetime.fromtimestamp(unix_timestamp)

    # Konvertieren Sie das datetime-Objekt in einen String
    string_timestamp = dt_object.strftime("%Y-%m-%d %H:%M:%S")

    return string_timestamp

def read_log(logfile):
    ping_times = []
    timestamps = []
    non_answers = []
    long_pings = []

    # Lesen Sie das Logfile und extrahieren Sie die Ping-Zeiten
    with open(logfile, "r") as file:
        for line in file:
            match = re.search(r"time=(\d+(\.\d+)?)", line)
            if match:
                ping_time = float(match.group(1))
                ping_times.append(ping_time)
            else:
                if line.find("no answer yet") != -1:
                    non_answers.append(line)
                else:
                    print(line, end="")

            match = re.search(r"\[(\d+\.\d+)\]", line)
            if match:
                timestamp = float(match.group(1))
                timestamps.append(timestamp)


    # Zähle die Anzahl der Unterbrechungen, die länger als 100ms dauern
    interruptions = 0
    for i in range(1, len(ping_times)):
        if ping_times[i] > 100:
            interruptions += 1
            long_pings.append(ping_times[i])

    # Berechnen Sie den frühesten und den neuesten Zeitstempel
    earliest_timestamp = min(timestamps)
    latest_timestamp = max(timestamps)

    # Berechnen Sie die Differenz zwischen dem frühesten und dem neuesten Zeitstempel
    time_difference = latest_timestamp - earliest_timestamp
    print()
    print("Start des Tests:", convert_timestamp_to_string(earliest_timestamp))
    print("Ende des Tests:", convert_timestamp_to_string(latest_timestamp))
    print("Anzahl der Antworten, die länger als 100ms gedauert haben:", interruptions)
    print("Längste Antwortzeit:", max(ping_times), "ms")
    print("Testdauer:", time_difference, "s")
    if len(non_answers)== 0:
        print("Keine verlorenen Pakete")
    else:
        print("Anzahl der verlorenen Pakete: {}, entspricht {:.1f}% oder ein Fehler alle {:.0f}s".format(len(non_answers), 100*len(non_answers)/(len(timestamps)), time_difference/len(non_answers) ))

    # Erstellen Sie ein Histogramm der Ping-Zeiten
    plt.hist(long_pings, bins=10)
    plt.xlabel("Ping-Zeit (ms)")
    plt.ylabel("Anzahl")
    plt.title("Ping-Zeiten Histogramm (nur pings > 100ms)")
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Bitte gib den Namen des Logfiles ein.")
        print("Logfile erzeugen mit 'ping -D -O www.google.com > pingoutput.txt'")
        #read_log("pingoutput.txt")
        sys.exit(1)

    read_log(sys.argv[1])

if __name__ == "__main__":
    main()
