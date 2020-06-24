import os
import base64

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
            print("Could not create path {}".format(path))
            return False
    print("Path {} found".format(path))
    return True

def create_file(path: str, filename: str, content: str):
    file_path = path + filename
    p_exists = path_exists(path)
    if p_exists == False:
        create_path(path)
    f_exists = file_exists(file_path)
    if f_exists == True:
        print("Overwriting {}".format(filename))
    
    try:
        file = open(file_path, "wb")
        formatted_content = bytearray(content)
        file.write(formatted_content)
        file.close()
        print("Created file {}".format(file_path))
        return True
    except Exception as e:
        print(e)
        print("Could not create file {}".format(file_path))
    
    return False

def open_file(file_path: str):
    f_exists = file_exists(file_path)
    if f_exists:
        return open(file_path, 'rb', buffering=0)