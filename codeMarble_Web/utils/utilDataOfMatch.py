# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarble_Web.model.problem import Problem
from codeMarble_Web.model.user import User
from codeMarble_Web.model.dataOfMatch import DataOfMatch
from codeMarble_Web.database import dao

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