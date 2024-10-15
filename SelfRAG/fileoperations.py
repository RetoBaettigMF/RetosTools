import os
import shutil
import glob

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def write_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def append_file(filename, text):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(text)

def get_files(path):
    files = []
    for file in os.listdir(path):
        files.append(os.path.join(path, file))
    return files

def change_file_type(filename, new_extension):
    name = os.path.basename(filename)
    path = os.path.dirname(filename)
    basename = os.path.splitext(name)[0]
    extension = os.path.splitext(name)[1]
    new_filename = os.path.join(path, basename + new_extension)
    return new_filename

def change_file_path(filename, new_path):
    name = os.path.basename(filename)
    new_filename = os.path.join(new_path, name)
    return new_filename

def get_file_extension(filename):
    name = os.path.basename(filename)
    extension = os.path.splitext(name)[1]
    return extension

def delete_directory(path):
    if os.path.exists(path):
        # Verzeichnis und alle Unterverzeichnisse löschen
        shutil.rmtree(path)
        print(f"Das Verzeichnis '{path}' wurde erfolgreich gelöscht.")
    else:
        print(f"Das Verzeichnis '{path}' existiert nicht.")
    