# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.userInformationInProblem import *
from codeMarbleWeb.model.user import *
from codeMarbleWeb.model.problem import *

from codeMarbleWeb.database import dao

def insert_userInformationInProblem(userIndex, problemIndex, score):
    return UserInformationInProblem(userIndex=userIndex, problemIndex=problemIndex, score=score)

def select_userInformationInProblem(userIndex=None, problemIndex=None):
    return dao.query(UserInformationInProblem).\
        filter(UserInformationInProblem.userIndex==userIndex if userIndex else UserInformationInProblem.userIndex!=userIndex,
               UserInformationInProblem.problemIndex==problemIndex if problemIndex else UserInformationInProblem.problemIndex==problemIndex)

def update_userInformationInProblem(userIndex, problemIndex, score):
    return dao.query(UserInformationInProblem).\
        filter(and_(UserInformationInProblem.userIndex==userIndex,
                    UserInformationInProblem.problemIndex==problemIndex)).\
        update(dict(score = score))

def get_total_score_each_users(userIndex=None):
    return dao.query(UserInformationInProblem.userIndex,
                     func.sum(UserInformationInProblem.score).label('totalScore')).\
                filter(UserInformationInProblem.userIndex == userIndex if userIndex
                        else UserInformationInProblem.userIndex != userIndex).\
                group_by(UserInformationInProblem.userIndex)

def get_topProblem():
    return dao.query(UserInformationInProblem.problemIndex,
                     func.count(UserInformationInProblem.problemIndex)).\
                group_by(UserInformationInProblem.problemIndex)