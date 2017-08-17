from sqlalchemy import and_

from codeMarble_Web.database import dao
from codeMarble_Web.model.problem import Problem


def insert_problem(problemName, placementRule, placementOption1, placementOption2, existRule, existOption, actionRule,
                   actionOption1, actionOption2, endingRule, endingOption, limitTime=1000, level=1, limitMemory=128):
	return Problem(problemName=problemName, placementRule=placementRule, placementOption1=placementOption1,
	               placementOption2=placementOption2, existRule=existRule, existOption=existOption,
	               actionRule=actionRule, actionOption1=actionOption1, actionOption2=actionOption2,
	               endingRule=endingRule, endingOption=endingOption, limitTime=limitTime, limitMemory=limitMemory,
	               level=level, isDelete=False)


def select_problem(problemIndex=None, problemName=None):
	if problemName:
		return dao.query(Problem). \
					filter(and_(Problem.problemName == problemName,
		                        Problem.isDelete == False))

	return dao.query(Problem).\
				filter(and_(Problem.problemIndex == problemIndex if problemIndex
	                        else Problem.problemIndex != problemIndex,
	                        Problem.isDelete == False))