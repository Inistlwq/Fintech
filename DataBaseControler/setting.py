#coding:utf-8
import os
SYSTEM_BASE_PATH = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
def database_path():
    path =os.path.join(SYSTEM_BASE_PATH,'DataBase')
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    return path
if __name__ =='__main__':
    print database_path()