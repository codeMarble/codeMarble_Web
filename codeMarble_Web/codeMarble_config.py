# -*- coding: utf-8 -*-
import os
from runServer import thisPath

configs = {'DBuser': 'root',
           'DBpassword': '',
           'DBIP': 'localhost',
           'redisIP': 'localhost',
           'redisPort': 6379,
           'webPort': 9410,
           'processCount': 2}

with open(os.path.join(thisPath, 'codeMarble.properties')) as fp:
    lines = fp.readlines()

    for line in lines:
        pos = line.find('#') if line.find('#') != -1 else len(line)
        line = line[:pos+1]

        if len(line) > 1:
            name, setting = [i.strip() for i in line.split('=')]
            configs[name] = setting

class codeMarbleConfig(object):
    DB_URL = "mysql+pymysql://{0}:{1}@{2}/codeMarble?charset=utf8".format(configs['DBuser'], configs['DBpassword'], configs['DBIP'])
    TMP_FOLDER = 'resource/tmp'
    PERMANENT_SESSION_LIFETIME = 60 * 60
    UPLOAD_FOLDER = '/mnt'
    CURRENT_FOLDER = '/mnt/shared/CurrentCourses'
    SESSION_COOKIE_NAME = 'codeMarble_session'
    LOG_LEVEL = 'debug'
    LOG_FILE_PATH = 'resource/log/codeMarble.log'
    DB_LOG_FLAG = 'True'