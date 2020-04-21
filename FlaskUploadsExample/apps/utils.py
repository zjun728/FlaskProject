import os


def creat_folder(folder_parth):
    if os.path.exists(folder_parth) == False:
        os.mkdir(folder_parth)  # 创建文件夹
        os.chmod(folder_parth, os.O_RDWR)  # 更改文件夹模式，可读可写
