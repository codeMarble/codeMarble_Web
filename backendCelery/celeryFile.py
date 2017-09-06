import os
import json
import random
import shutil
from celery import Celery

from codeMarble.gameManager import GameManager
from codeMarble.userProgram import UserProgram
from codeMarble.execution import Execution
from codeMarble_Web.database import dao

from codeMarble_Web.utils.utilCodeQuery import select_code
from codeMarble_Web.utils.utilLanguageQuery import select_language


app = Celery('tasks', broker='redis://localhost:6379')

try:
	dataDir = os.path.join(os.getcwd(), 'problemData')
	tempDir = os.path.join(os.getcwd(), 'tempData')
	os.mkdir(dataDir)
	os.mkdir(tempDir)
except Exception as e:
	pass


class SqlAlchemyTask(app.Task):
	abstract = True

	def after_return(self, status, retval, task_id, args, kwargs, einfo):
		dao.remove()


@app.task(name='task.addProblem')
def addProblem(jsonData, problemIndex):
	with open(os.path.join(dataDir, '%i.json'%problemIndex), 'w', encoding='utf-8') as fp:
		json.dump(jsonData, fp)


@app.task(name='task.compileCode', base=SqlAlchemyTask)
def compileCode(codeIndex):
	codeData = select_code(codeIndex=codeIndex).first()
	codePath = os.path.join(tempDir, '%d.txt'%codeIndex)
	language = select_language(languageIndex=codeData.languageIndex).first().language
	execution = Execution()

	with open(codePath, 'w') as fp:
		fp.write(codeData.code)

	user = UserProgram(language=language, savePath=tempDir, fileName='%d.txt'%codeIndex)
	result = execution.executeProgram(user.compile())

	os.remove(codePath)
	os.remove(user.executionPath)

	if result is True:
		pass

	else:
		pass


@app.task(name='task.matching', base=SqlAlchemyTask)
def matching(problemIndex, challengerIndex, championIndex):
	temp = '{0}{1}{2}{3}'.format(problemIndex, challengerIndex, championIndex, random.randint(10, 99))
	tempPath = os.path.join(tempDir, temp)

	challengerCodeData = select_code(problemIndex=problemIndex, userIndex=challengerIndex).first()
	championCodeData = select_code(problemIndex=problemIndex, userIndex=championIndex).first()

	challengerCodePath = os.path.join(tempPath, '{0}.txt'.format(challengerCodeData.codeIndex))
	championCodePath = os.path.join(tempPath, '{0}.txt'.format(championCodeData.codeIndex))

	challengerLanguage = select_language(languageIndex=challengerCodeData.languageIndex).first().language
	championLanguage = select_language(languageIndex=championCodeData.languageIndex).first().language

	with open(challengerCodePath, 'w') as fp:
		fp.write(challengerCodeData.code)

	with open(championCodePath, 'w') as fp:
		fp.write(championCodeData.code)

	with open(os.path.join(dataDir ,'{0}.json')) as fp:
		data = json.load(fp)

	challenger = UserProgram(language=challengerLanguage, savePath=tempPath, fileName='%d.txt' % challengerCodeData.codeIndex)
	champion = UserProgram(language=championLanguage, savePath=tempPath, fileName='%d.txt' % championCodeData.codeIndex)

	gameManager = GameManager(challenger=challenger, champion=champion, placementRule=data['placementRule'],
	                          placementOption=data['placementOption'], existRule=data['existRule'], existOption=data['existOption'],
	                          actionRule=data['actionRule'], actionOption=data['actionOption'], endingRule=data['endingRule'],
	                          endingOption=data['endingOption'], gameBoard=data['gameBoard'], dataBoard=data['dataBoard'])

	result = gameManager.playGame()

	# shutil.rmtree(tempPath)

























