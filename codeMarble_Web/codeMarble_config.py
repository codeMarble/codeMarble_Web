# -*- coding: utf-8 -*-
import os
from runServer import thisPath
from codeMarble_Web.codeMarble_propertyParser import configs, propertyParser


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