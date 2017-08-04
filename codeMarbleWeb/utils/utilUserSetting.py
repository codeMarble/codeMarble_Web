# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.user import User
from codeMarbleWeb.model.userSetting import UserSetting
from codeMarbleWeb.database import dao

def insert_userSetting(userIndex, languageIndex, thema, comment):
    return UserSetting(userIndex=userIndex, languageIndex=languageIndex,
                       thema=thema, comment=comment, isCodeOpen=False)

def select_userSetting(userIndex):
    return dao.query(UserSetting).\
        filter(UserSetting.userIndex==userIndex)

def update_userSetting(userIndex):
    return dao.query(UserSetting).\
        filter(and_(UserSetting.userIndex==userIndex)).\
        update(dict(isCodeOpen = True))