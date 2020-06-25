import os
import base64
from pathlib import Path

def path_exists(path: str):
    return os.path.isdir(path)

def file_exists(file_path: str):
    return os.path.isfile(file_path)

def create_path(path: str):
    exists = path_exists(path)
    if exists == False:
        try:
            os.mkdir(path)
            return True
        except:
            print(".. Could not create path {}".format(path))
            return False
    print("Path {} found".format(path))
    return True

def create_file(path: str, filename: str, content: str):
    file_path = path + filename
    print("- Creating file at {}".format(file_path))
    p_exists = path_exists(path)
    if p_exists == False:
        create_path(path)
    f_exists = file_exists(file_path)
    if f_exists == True:
        print(".. Found existing file. Overwriting {}".format(filename))
    
    formatted_content = bytearray(content)
    try:
        with open(file_path, "wb") as writer:
            writer.write(formatted_content)
            print(".. Created file.")
            return True
    except Exception as e:
        print(".. Could not create file {}".format(file_path))
        print(e)
    
    return False

def open_file(file_path: str, mode: str):
    print(".. Opening file at {}".format(file_path))
    f_exists = file_exists(file_path)
    if f_exists:
        with open(file_path, mode, buffering=0) as reader:
            try:
                file_content = reader.read()
                print(".. ## FILE CONTENT ##")
                print(file_content)
                return file_content
            except:
                print(".. Error opening file at {}".format(file_path))
    return False