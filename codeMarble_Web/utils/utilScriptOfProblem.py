# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarble_Web.model.problem import Problem
from codeMarble_Web.model.scriptOfProblem import ScriptOfProblem

from codeMarble_Web.database import dao

def insert_scriptOfProblem(problemIndex, userScript):
    return ScriptOfProblem(problemIndex=problemIndex, userScript=userScript)

def select_scriptOfProblem(problemIndex):
    return dao.query(ScriptOfProblem).\
        filter(ScriptOfProblem.problemIndex==problemIndex)