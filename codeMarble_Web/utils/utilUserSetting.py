# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarble_Web.model.user import User
from codeMarble_Web.model.userSetting import UserSetting
from codeMarble_Web.database import dao

def insert_userSetting(userIndex, languageIndex, thema, comment):
    return UserSetting(userIndex=userIndex,
                       languageIndex=languageIndex,
                       thema=thema,
                       comment=comment,
                       isOpen=False)

def select_userSetting(userIndex):
    return dao.query(UserSetting).\
        filter(UserSetting.userIndex==userIndex)

def update_userSetting(userIndex, languageIndex, thema, comment, isOpen):
    return dao.query(UserSetting).\
        filter(UserSetting.userIndex==userIndex).\
        update(dict(languageIndex=languageIndex,
                    thema=thema,
                    comment=comment,
                    isOpen=isOpen))