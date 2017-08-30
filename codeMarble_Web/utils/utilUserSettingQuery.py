# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarble_Web.model.user import User
from codeMarble_Web.model.userSetting import UserSetting
from codeMarble_Web.database import dao

def insert_userSetting(userIndex, languageIndex=1, thema='chrome', comment=''):
    return UserSetting(userIndex=userIndex,
                       languageIndex=languageIndex,
                       thema=thema,
                       comment=comment,
                       isOpen=True)

def select_userSetting(userIndex):
    return dao.query(UserSetting).\
        filter(UserSetting.userIndex==userIndex)

def update_userSetting(userIndex, languageIndex=None, thema=None, comment=None, isOpen=None):
    dao.query(UserSetting).\
        filter(UserSetting.userIndex==userIndex).\
        update(dict(languageIndex=languageIndex if languageIndex else UserSetting.languageIndex,
                    thema=thema if thema else UserSetting.thema,
                    comment=comment if comment else UserSetting.comment,
                    isOpen=isOpen if isOpen else UserSetting.isOpen))

def get_user_information(userIndex):
    subQ = dao.query(User).filter(User.userIndex == userIndex).subquery()

    return dao.query(subQ.c.userId, subQ.c.nickName, subQ.c.eMail, UserSetting.languageIndex, UserSetting.userIndex,
                     UserSetting.thema, UserSetting.comment, UserSetting.isOpen).\
                join(UserSetting,
                     subQ.c.userIndex == UserSetting.userIndex)