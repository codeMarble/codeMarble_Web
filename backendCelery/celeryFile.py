import os
import json
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

	if result is True:
		pass

	else:
		pass


@app.task(name='task.matching', base=SqlAlchemyTask)
def matching(problemIndex, challengerIndex, championIndex):
	challengerCodeData = select_code(problemIndex=problemIndex, userIndex=challengerIndex).first()
	championCodeData = select_code(problemIndex=problemIndex, userIndex=championIndex).first()

	challengerCodePath = os.path.join(tempDir, '%d.txt' % challengerCodeData.codeIndex)
	championCodePath = os.path.join(tempDir, '%d.txt' % championCodeData.codeIndex)

	challengerLanguage = select_language(languageIndex=challengerCodeData.languageIndex).first().language
	championLanguage = select_language(languageIndex=championCodeData.languageIndex).first().language

	with open(challengerCodePath, 'w') as fp:
		fp.write(challengerCodeData.code)

	with open(championCodePath, 'w') as fp:
		fp.write(championCodeData.code)

	challenger = UserProgram(language=challengerLanguage, savePath=tempDir, fileName='%d.txt' % challengerCodeData.codeIndex)
	champion = UserProgram(language=championLanguage, savePath=tempDir, fileName='%d.txt' % championCodeData.codeIndex)

	# gameManager = GameManager(challenger=challenger, champion=champion, )
	# challenger, champion, placementRule, placementOption, existRule, existOption,
	# actionRule, actionOption, endingRule, endingOption, gameBoard, dataBoard, scriptPath = None, problemIndex = 'scriptTemplate'



























