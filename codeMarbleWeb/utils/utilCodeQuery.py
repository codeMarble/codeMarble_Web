# -*- coding: utf-8 -*-

from sqlalchemy import and_

from codeMarbleWeb.model.code import Code
from codeMarbleWeb.model.user import User
from codeMarbleWeb.model.problem import Problem
from codeMarbleWeb.model.language import Language

from codeMarbleWeb.database import dao


def insert_code(userIndex, problemIndex, languageIndex, code):
    return Code(userIndex=userIndex, problemIndex=problemIndex,
                languageIndex=languageIndex, code=code, isOpen=False)

def select_code(userIndex, problemIndex, languageIndex):
    return dao.query(Code).\
            filter(and_(Code.userIndex == userIndex,
                        Code.problemIndex == problemIndex,
                        Code.languageIndex == languageIndex))