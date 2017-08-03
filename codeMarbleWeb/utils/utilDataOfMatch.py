# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.problem import Problem
from codeMarbleWeb.model.user import User
from codeMarbleWeb.model.dataOfMatch import DataOfMatch
from codeMarbleWeb.database import dao

def insert_dataOfMatch(problemIndex, challengerIndex, championIndex, positionData, boardData):
    return DataOfMatch(ProblemIndex=problemIndex, challengerIndex=challengerIndex,championIndex=championIndex,
                       result = '...ing...', positionData=positionData, boardData=boardData)


def select_dataOfMatch(problemIndex, challengerIndex, championIndex):
    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex==problemIndex,
                            DataOfMatch.challengerIndex==challengerIndex,
                            DataOfMatch.championIndex==championIndex))

def update_dataOfMatch_win(problemIndex, challengerIndex, championIndex):
    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex==problemIndex,
                            DataOfMatch.challengerIndex==challengerIndex,
                            DataOfMatch.championIndex==championIndex)).\
                update(dict(result='win'))

def update_dataOfMatch_lose(problemIndex, challengerIndex, championIndex):
    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex==problemIndex,
                            DataOfMatch.challengerIndex==challengerIndex,
                            DataOfMatch.championIndex==championIndex)).\
                update(dict(result='lose'))

def update_dataOfMatch_draw(problemIndex, challengerIndex, championIndex):
    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex==problemIndex,
                            DataOfMatch.challengerIndex==challengerIndex,
                            DataOfMatch.championIndex==championIndex)).\
                update(dict(result='draw'))

def update_dataOfMatch_serveError(problemIndex, challengerIndex, championIndex):
    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex==problemIndex,
                            DataOfMatch.challengerIndex==challengerIndex,
                            DataOfMatch.championIndex==championIndex)).\
                update(dict(result='server error'))