import os
import sys
import json
import random
import shutil

thisPath, _ = os.path.split(os.path.abspath(__file__))
sys.path.insert(0, os.path.split(thisPath)[0])


from celery import Celery
from codeMarble_Web.database import DBManager


app = Celery('tasks', broker='redis://localhost:6379')
DBManager.init('mysql+pymysql://root:@localhost/codeMarble?charset=utf8')


from codeMarble.gameManager import GameManager
from codeMarble.userProgram import UserProgram
from codeMarble.execution import Execution

from codeMarble_Web.utils.utilUserInformationInProblem import select_userInformationInProblem, update_userInformationInProblem
from codeMarble_Web.utils.utilCodeQuery import select_code, update_code, select_recent_code
from codeMarble_Web.utils.utilDataOfMatch import update_dataOfMatch_result, select_dataOfMatch
from codeMarble_Web.utils.utilLanguageQuery import select_language


try:
	dataDir = os.path.join(os.getcwd(), 'problemData')
	tempDir = os.path.join(os.getcwd(), 'tempData')
	os.mkdir(dataDir)
	os.mkdir(tempDir)
except Exception as e:
	pass


from codeMarble_Web.database import dao

class SqlAlchemyTask(app.Task):
	abstract = True

	def after_return(self, status, retval, task_id, args, kwargs, einfo):
		dao.remove()


extension = ['', '.c', '.cpp', '.py', '.py', '.java']
@app.task(name='task.addProblem')
def addProblem(problemIndex, jsonData):
	jsonData = json.loads(jsonData)
	try:
		with open(os.path.join(dataDir, '{0}.json'.format(problemIndex)), 'w') as fp:
			json.dump(jsonData, fp)

		return True

	except Exception as e:
		print e
		return False


@app.task(name='task.compileCode', base=SqlAlchemyTask)
def compileCode(codeIndex):
	codeData = select_code(codeIndex=codeIndex).first()

	try:
		if 2 < codeData.languageIndex < 5:
			update_code(codeIndex=codeIndex, isCompile=True)
			dao.commit()

		else:
			fileName = '{0}{1}'.format(codeIndex, extension[codeData.languageIndex])

			codePath = os.path.join(tempDir, fileName)
			language = select_language(languageIndex=codeData.languageIndex).first().language
			execution = Execution()

			with open(codePath, 'w') as fp:
				fp.write(codeData.code)

			user = UserProgram(language=language, savePath=tempDir, fileName=fileName)
			_, _, result = execution.executeProgram(user.compile(), user.savePath)

			os.remove(codePath)

			if result is True:
				os.remove(user.executionPath)
				update_code(codeIndex=codeIndex, isCompile=True)

				dao.commit()

	except Exception as e:
		print e
		dao.rollback()


@app.task(name='task.matching', base=SqlAlchemyTask)
def matchingGame(problemIndex, challengerIndex, championIndex):
	try:
		matchIndex = select_dataOfMatch(problemIndex=problemIndex, challengerIndex=challengerIndex,
		                                championIndex=championIndex).all()[-1].dataOfMatchIndex

		temp = '{0}{1}{2}{3}'.format(problemIndex, challengerIndex, championIndex, random.randint(1000, 9999))
		tempPath = os.path.join(tempDir, temp)
		os.mkdir(tempPath)

		challengerCodeData = select_recent_code(problemIndex=problemIndex, userIndex=challengerIndex).first()
		championCodeData = select_recent_code(problemIndex=problemIndex, userIndex=championIndex).first()

		challengerCodeData = select_code(codeIndex=challengerCodeData.leastIndex).first()
		championCodeData = select_code(codeIndex=championCodeData.leastIndex).first()

		challengerFileName = '{0}{1}'.format(challengerIndex, extension[challengerCodeData.languageIndex])
		championFileName = '{0}{1}'.format(championIndex, extension[championCodeData.languageIndex])

		challengerCodePath = os.path.join(tempPath, challengerFileName)
		championCodePath = os.path.join(tempPath, championFileName)

		challengerLanguage = select_language(languageIndex=challengerCodeData.languageIndex).first().language
		championLanguage = select_language(languageIndex=championCodeData.languageIndex).first().language

		with open(challengerCodePath, 'w') as fp:
			fp.write(challengerCodeData.code)

		with open(championCodePath, 'w') as fp:
			fp.write(championCodeData.code)

		with open(os.path.join(dataDir, '{0}.json'.format(problemIndex))) as fp:
			data = json.load(fp)

		challenger = UserProgram(language=challengerLanguage, savePath=tempPath, fileName=challengerFileName)
		champion = UserProgram(language=championLanguage, savePath=tempPath, fileName=championFileName)

		gameManager = GameManager(challenger=challenger, champion=champion, placementRule=data["placementRule"],
		                          placementOption=data['placementOption'], existRule=data['existRule'], existOption=data['existOption'],
		                          actionRule=data['actionRule'], actionOption=data['actionOption'], endingRule=data['endingRule'],
		                          endingOption=data['endingOption'], gameBoard=data['gameBoard'], dataBoard=data['dataBoard'],
		                          objectCount=data['objectCount'])

		result, positionData, boardData = gameManager.playGame()

		shutil.rmtree(tempPath)

		challengerScoreData = select_userInformationInProblem(userIndex=challengerIndex, problemIndex=problemIndex).first()
		championScoreData = select_userInformationInProblem(userIndex=championIndex, problemIndex=problemIndex).first()

		diffScore = abs(challengerScoreData.score - championScoreData.score)
		diffScore = diffScore if diffScore <= 300 else 300
		addScoreForChallenger, addScoreForChampion = 0, 0

		if result == 'win':
			addScoreForChallenger = 10 + int(diffScore*0.11) if diffScore > 15 else 10
			addScoreForChampion = -(addScoreForChallenger // 3)

		elif result == 'lose' and challengerScoreData.score > 0:
			addScoreForChallenger = -16 + int(diffScore*0.05) if diffScore > 15 else -16
			addScoreForChampion = abs(addScoreForChallenger)


		update_userInformationInProblem(userIndex=challengerIndex, problemIndex=problemIndex, score=addScoreForChallenger)
		update_userInformationInProblem(userIndex=championIndex, problemIndex=problemIndex, score=addScoreForChampion)

		update_dataOfMatch_result(dataOfMatchIndex=matchIndex, result=result, positionData=positionData, boardData=boardData)

		dao.commit()
		print matchIndex, result

	except Exception as e:
		print e, sys.exc_info()[2].tb_lineno
		dao.rollback()

		update_dataOfMatch_result(dataOfMatchIndex=matchIndex, result='server error')

		dao.commit()







