# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.problem import Problem
from codeMarbleWeb.model.user import User
from codeMarbleWeb.model.dataOfMatch import DataOfMatch
from codeMarbleWeb.database import dao

def insert_dataOfMatch(problemIndex, challengerIndex, championIndex, positionData, boardData):
    return DataOfMatch(ProblemIndex=problemIndex, challengerIndex=challengerIndex,championIndex=championIndex,
                        result = '...ing...', positionData=positionData, boardData=boardData)

def select_dataOfMatch(problemIndex=None, challengerIndex=None, championIndex=None, dataOfMatchIndex=None):
    if dataOfMatchIndex:
        return dao.query(DataOfMatch).\
                    filter(DataOfMatch.dataOfMatchIndex == dataOfMatchIndex)

    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex == problemIndex if problemIndex
                            else DataOfMatch.problemIndex != problemIndex,
                            DataOfMatch.challengerIndex == challengerIndex if challengerIndex
                            else DataOfMatch.challengerIndex != challengerIndex,
                            DataOfMatch.championIndex == championIndex if championIndex
                            else DataOfMatch.championIndex == championIndex))

def update_dataOfMatch_result(problemIndex, challengerIndex, championIndex, result, dataOfMatchIndex=None):
    if dataOfMatchIndex:
        return dao.query(DataOfMatch).\
                    filter(DataOfMatch.dataOfMatchIndex == dataOfMatchIndex).\
                    update(dict(result=result))

    return dao.query(DataOfMatch).\
                filter(and_(DataOfMatch.problemIndex==problemIndex,
                            DataOfMatch.challengerIndex==challengerIndex,
                            DataOfMatch.championIndex==championIndex)).\
                update(dict(result=result))