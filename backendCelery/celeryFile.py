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

from codeMarble_Web.utils.utilCodeQuery import select_code, update_code
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
def addProblem(jsonData, problemIndex):
	with open(os.path.join(dataDir, '{0}.json'.format(problemIndex)), 'w', encoding='utf-8') as fp:
		json.dump(jsonData, fp)


@app.task(name='task.compileCode', base=SqlAlchemyTask)
def compileCode(codeIndex):
	codeData = select_code(codeIndex=codeIndex).first()
	fileName = '{0}{1}'.format(codeIndex, extension[codeData.languageIndex])

	codePath = os.path.join(tempDir, fileName)
	language = select_language(languageIndex=codeData.languageIndex).first().language
	execution = Execution()

	with open(codePath, 'w') as fp:
		fp.write(codeData.code)

	try:
		user = UserProgram(language=language, savePath=tempDir, fileName=fileName)
		_, _, result = execution.executeProgram(user.compile())

		os.remove(codePath)

		if result is True:
			os.remove(user.executionPath)
			update_code(codeIndex=codeIndex, isCompile=True)

			dao.commit()

	except Exception as e:
		print e


@app.task(name='task.matching', base=SqlAlchemyTask)
def matching(problemIndex, challengerIndex, championIndex):
	temp = '{0}{1}{2}{3}'.format(problemIndex, challengerIndex, championIndex, random.randint(10, 99))
	tempPath = os.path.join(tempDir, temp)

	challengerCodeData = select_code(problemIndex=problemIndex, userIndex=challengerIndex).first()
	championCodeData = select_code(problemIndex=problemIndex, userIndex=championIndex).first()

	challengerFileName = '{0}{1}'.format(challengerCodeData.codeIndex, extension[challengerCodeData.languageIndex])
	championFileName = '{0}{1}'.format(championCodeData.codeIndex, extension[championCodeData.languageIndex])

	challengerCodePath = os.path.join(tempPath, challengerFileName)
	championCodePath = os.path.join(tempPath, championFileName)

	challengerLanguage = select_language(languageIndex=challengerCodeData.languageIndex).first().language
	championLanguage = select_language(languageIndex=championCodeData.languageIndex).first().language

	with open(challengerCodePath, 'w') as fp:
		fp.write(challengerCodeData.code)

	with open(championCodePath, 'w') as fp:
		fp.write(championCodeData.code)

	with open(os.path.join(dataDir ,'{0}.json')) as fp:
		data = json.load(fp)

	challenger = UserProgram(language=challengerLanguage, savePath=tempPath, fileName=challengerFileName)
	champion = UserProgram(language=championLanguage, savePath=tempPath, fileName=championFileName)

	gameManager = GameManager(challenger=challenger, champion=champion, placementRule=data['placementRule'],
	                          placementOption=data['placementOption'], existRule=data['existRule'], existOption=data['existOption'],
	                          actionRule=data['actionRule'], actionOption=data['actionOption'], endingRule=data['endingRule'],
	                          endingOption=data['endingOption'], gameBoard=data['gameBoard'], dataBoard=data['dataBoard'])

	result = gameManager.playGame()

	shutil.rmtree(tempPath)

























