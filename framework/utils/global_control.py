
from enum import Enum, unique

@unique
class LogLevel(Enum):
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4
@unique
class FileType(Enum):
    VIDEO = 1
    IMAGE = 0
@unique
class CalledType(Enum):
    KFZ = 0
    FBS = 1


GLOBAL_KFZURL = ""     #全局变量，控制访问哪个开发者中心
GLOBAL_FBSURL = ""     #全局变量，控制访问哪个菠萝
GLOBAL_USERINFO = {"appKey":"usernamestr","appSecret":"passwordstr"}

def setURL(kfz,fbs= "http://10.20.101.110:32345"):
    global GLOBAL_KFZURL,GLOBAL_FBSURL
    GLOBAL_KFZURL = kfz
    GLOBAL_FBSURL = fbs

def setUserInfo(appKey,appSecret):
    global GLOBAL_USERINFO
    GLOBAL_USERINFO["appKey"] = appKey
    GLOBAL_USERINFO["appSecret"] = appSecret

def setFaceLib(libId = ""):
    with open("../libId.config",'w', errors="ignore") as f:
        f.write(libId)

def getHost(calledBy):
    if calledBy == CalledType.FBS:
        global GLOBAL_FBSURL
        return GLOBAL_FBSURL
    else:
        global GLOBAL_KFZURL
        return GLOBAL_KFZURL

def getFaceLib():
    with open("../libId.config", 'r', errors="ignore") as f:
        faceLibId = f.read()
    return faceLibId

def getUserInfo():
    global GLOBAL_USERINFO
    return GLOBAL_USERINFO

    return TCList