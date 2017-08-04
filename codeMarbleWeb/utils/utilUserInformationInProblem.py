# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.userInformationInProblem import *
from codeMarbleWeb.model.user import *
from codeMarbleWeb.model.problem import *

from codeMarbleWeb.database import dao

def insert_userInformationInProblem(userIndex, problemIndex, score):
    return UserInformationInProblem(userIndex=userIndex, problemIndex=problemIndex, score=score)

def select_userInformationInProblem(userIndex, problemIndex):
    return dao.query(UserInformationInProblem).\
        filter(UserInformationInProblem.userIndex==userIndex,
               UserInformationInProblem.problemIndex==problemIndex)

def update_userInformationInProblem(userIndex, problemIndex, score):
    return dao.query(UserInformationInProblem).\
        filter(and_(UserInformationInProblem.userIndex==userIndex,
                    UserInformationInProblem.problemIndex==problemIndex)).\
        update(dict(score = score))