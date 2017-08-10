# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.user import User
from codeMarbleWeb.model.userSetting import UserSetting
from codeMarbleWeb.database import dao

def insert_userSetting(userIndex, languageIndex, thema, comment):
    return UserSetting(userIndex=userIndex, languageIndex=languageIndex,
                       thema=thema, comment=comment, isOpen=False)

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