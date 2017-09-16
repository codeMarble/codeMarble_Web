from sqlalchemy import and_

from codeMarble_Web.database import dao
from codeMarble_Web.model.problem import Problem


def insert_problem(problemName, placementRule, placementOption, existRule, existOption, actionRule, actionOption,
                   endingRule, endingOption, gameBoard, dataBoard, limitTime=2000, limitMemory=128, level=1):
	return Problem(problemName=problemName, placementRule=placementRule, placementOption=placementOption,
	               existRule=existRule, existOption=existOption, actionRule=actionRule, actionOption=actionOption,
	               endingRule=endingRule, endingOption=endingOption, gameBoard=gameBoard, dataBoard=dataBoard,
	               limitTime=limitTime, limitMemory=limitMemory, level=level, isDelete=False)


def select_problem(problemIndex=None, problemName=None):
	if problemName:
		return dao.query(Problem). \
					filter(and_(Problem.problemName == problemName,
		                        Problem.isDelete == False))

	return dao.query(Problem).\
				filter(and_(Problem.problemIndex == problemIndex if problemIndex
	                        else Problem.problemIndex != problemIndex,
	                        Problem.isDelete == False))