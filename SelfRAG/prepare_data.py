import os
from settings import DATA_PATH, PREPARED_DATA_PATH
from preparefiles import prepare_files
    
def convert_file(subdir, filename, outfile):
    if os.path.isfile(os.path.join(subdir, filename)):
        # Schreiben Sie den Dateinamen in das gewünschte Format
        subdir_name = os.path.basename(subdir)
        
        print(f"Füge Datei {filename} aus '{subdir_name}' an\n")
        outfile.write(f"*** FILENAME: \"{filename}\" ***\n")
        
        # Öffnen und lesen Sie den Inhalt der aktuellen Datei
        with open(os.path.join(subdir, filename), 'r', encoding='utf-8') as infile:
            # Schreiben Sie den Inhalt in die Ausgabedatei
            outfile.write(infile.read())
        
        # Fügen Sie 4 Leerzeilen am Ende jeder Datei hinzu
        outfile.write("\n\n\n\n")


def prepare_data():
    print("Preparing files...")
    prepare_files(DATA_PATH, PREPARED_DATA_PATH)

    print("Generating concatenated files...")
    # Definieren Sie den Pfad zum Hauptverzeichnis
    main_directory = PREPARED_DATA_PATH

    # Durchlaufen Sie alle Unterverzeichnisse im Hauptverzeichnis
    for subdir, _, files in os.walk(main_directory):
    # Definieren Sie den Namen der Ausgabedatei für das aktuelle Unterverzeichnis
        subdir_name = os.path.basename(subdir)
        output_file = os.path.join(os.getcwd(), f"{subdir_name}.txt")

        # Öffnen Sie die Ausgabedatei im Schreibmodus
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Durchlaufen Sie alle Dateien im aktuellen Unterverzeichnis
            for filename in files:
                convert_file(subdir, filename, outfile)

        print(f"Alle Dateien aus '{subdir_name}' wurden in '{output_file}' zusammengefügt.")

if __name__ == "__main__":
    prepare_data()