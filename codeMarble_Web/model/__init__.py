# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ['user', 'code', 'board', 'replyOfBoard', 'language',
           'userInformationInProblem', 'dataOfMatch', 'scriptOfProblem',
           'userSetting', 'notice', 'problem']