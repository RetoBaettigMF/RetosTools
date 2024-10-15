import os

# Definieren Sie den Pfad zum Unterverzeichnis
directory = "prepareddata"

# Definieren Sie den Namen der Ausgabedatei
output_file = "combined_output.txt"

# Öffnen Sie die Ausgabedatei im Schreibmodus
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Durchlaufen Sie alle Dateien im Verzeichnis
    for filename in os.listdir(directory):
        # Stellen Sie sicher, dass es sich um eine Datei handelt (nicht um ein Unterverzeichnis)
        if os.path.isfile(os.path.join(directory, filename)):
            # Schreiben Sie den Dateinamen in das gewünschte Format
            print(f"Füge Datei {filename} an\n")
            outfile.write(f"*** FILENAME: \"{filename}\" ***\n")
            
            # Öffnen und lesen Sie den Inhalt der aktuellen Datei
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as infile:
                # Schreiben Sie den Inhalt in die Ausgabedatei
                outfile.write(infile.read())
            
            # Fügen Sie 4 Leerzeilen am Ende jeder Datei hinzu
            outfile.write("\n\n\n\n")

print(f"Alle Dateien wurden in '{output_file}' zusammengefügt.")
