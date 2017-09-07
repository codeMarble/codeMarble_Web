# -*- coding: utf-8 -*-

from sqlalchemy import and_

from codeMarble_Web.model.code import Code
from codeMarble_Web.model.user import User
from codeMarble_Web.model.problem import Problem
from codeMarble_Web.model.language import Language

from codeMarble_Web.database import dao


def insert_code(userIndex, problemIndex, languageIndex, date, code, isOpen=True):
    return Code(userIndex=userIndex,
                problemIndex=problemIndex,
                languageIndex=languageIndex,
                code=code,
                date=date,
                isCompile=False,
                isOpen=isOpen)

def select_code(userIndex=None, problemIndex=None, languageIndex=None, isCompile=None, codeIndex=None):
    if codeIndex:
        return dao.query(Code).\
                    filter(Code.codeIndex == codeIndex)

    return dao.query(Code).\
                filter(and_(Code.userIndex == userIndex if userIndex
                            else Code.userIndex != userIndex,
                            Code.problemIndex == problemIndex if problemIndex
                            else Code.problemIndex != problemIndex,
                            Code.languageIndex == languageIndex if languageIndex
                            else Code.languageIndex != languageIndex,
                            Code.isCompile == isCompile if isCompile is not None
                            else Code.isCompile != isCompile))


def update_code(codeIndex, date=None, isCompile=None, isOpen=None):
    return dao.query(Code).\
                filter(Code.codeIndex == codeIndex).\
                update(dict(date=date if date else Code.date,
                            isCompile=isCompile if isCompile is not None else Code.isCompile,
                            isOpen=isOpen if isOpen is not None else Code.isOpen))