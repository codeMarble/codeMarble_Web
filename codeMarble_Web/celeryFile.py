from celery import Celery
from codeMarble_config import configs


app = Celery('tasks', broker='redis://{0}:{1}'.format(configs['redisIP'], configs['redisPort']))


@app.task(name='task.addProblem')
def addProblem(problemIndex, jsonData):
	pass


@app.task(name='task.compileCode')
def compileCode(codeIndex):
	pass


@app.task(name='task.matching')
def matchingGame(problemIndex, challengerIndex, championIndex):
	pass
























