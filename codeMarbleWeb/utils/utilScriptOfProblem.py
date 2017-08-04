# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.problem import Problem
from codeMarbleWeb.model.scriptOfProblem import ScriptOfProblem

from codeMarbleWeb.database import dao

def insert_scriptOfProblem(problemIndex, userScript):
    return ScriptOfProblem(problemIndex=problemIndex, userScript=userScript)

def select_scriptOfProblem(problemIndex):
    return dao.query(ScriptOfProblem).\
        filter(ScriptOfProblem.problemIndex==problemIndex)