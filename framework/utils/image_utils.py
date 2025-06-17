#common.py

"""
通用API
author:slg
date:2022/8/18
"""

import base64
import os
import re
from stat import S_ISDIR, S_ISREG

# 是否图片文件
def is_image_file(file_name):
    name = file_name.lower()
    extension = name[name.rfind('.')+1:]
        
    s = re.match("jpg|jpeg|jpe|jfif|bmp|png|gif", extension)
    return s != None


# 读取文件，返回二进制数据
def read_image(file_name):
    """ read image file """
    if file_name == None or len(file_name) < 4:
        print("文件名不合法")
        return None

    if not is_image_file(file_name):
        print("不是图片文件")
        return None    

    if os.stat(file_name).st_size <= 0:
        print("文件为空")
        return None
    
    if os.path.isfile(file_name):
        # image exists
        try:
            f = open(file_name, 'br')
            data = f.read()
            f.close()
            return data
        except:
            return None
    else:
        # image no exists
        print("file no exists: " + file_name)
        return None


# base64编码，返回的字符串去掉前边的b
def base64_encode(data):
    b64_data = base64.b64encode(data)   # 二进制图片 -> base64字节码
    return b64_data.decode('ascii')   # base64字节码 -> 普通字符串，去掉前边的b


# 查询当前目录下所有图片文件名称的字符串列表，包含子目录
def folders_list_images(path, deepth=1):
    """
    path:指定的文件夹
    """    
    if not os.path.exists(path):
        print("不是合法的目录")
        return []
    
    if not os.path.isdir(path):
        print("不是合法的目录")
        return []
    
    p = path
    p = p.replace("/","\\")
    if p[-1] != "\\":
        p = p + "\\"

    img_list = []
    
    name = ""

    try:
        name = p
        list_temp = os.listdir(p)

        for f in list_temp:
            name = os.path.join(p, f)
          
            mode = os.stat(name).st_mode
            if S_ISDIR(mode):
                sublist = folders_list_images(name + "\\", deepth + 1)
                if len(sublist) > 0:
                    img_list = img_list + sublist
            elif S_ISREG(mode) and is_image_file(name):
                img_list.append(name)
    except:
        print("捕获到访问异常:" + str(deepth) + " - " + name)
        
    return img_list

#以round-robin的方式拆分为子列表
def round_robin_sublists(ls, splitcount=4):
    lists = [[] for _ in range(splitcount)]
    i = 0
    for elem in ls:
        lists[i].append(elem)
        i = (i + 1) % splitcount
    return lists


if __name__ == '__main__':
    list = folders_list_images(r"E:\自动化\auto_2025\yinghua\data\ai_perf")
    for i in list:
        print(i)

