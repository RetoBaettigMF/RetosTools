import os
import glob

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def write_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def get_files(path):
    files = []
    for file in os.listdir(path):
        files.append(os.path.join(path, file))
    return files

def delete_directory(path):
    file_list = glob.glob(path+"/*")
    for file_path in file_list:
        os.remove(file_path)
    