# -*- coding: utf-8 -*-

class codeMarbleConfig(object):
    DB_URL = "mysql+pymysql://root:@localhost/codeMarble?charset=utf8"
    TMP_FOLDER = 'resource/tmp'
    PERMANENT_SESSION_LIFETIME = 60* 60
    UPLOAD_FOLDER = '/mnt'
    CURRENT_FOLDER = '/mnt/shared/CurrentCourses'
    SESSION_COOKIE_NAME = 'codeMarble_session'
    LOG_LEVEL = 'debug'
    LOG_FILE_PATH = 'resource/log/codeMarble.log'
    DB_LOG_FLAG = 'True'