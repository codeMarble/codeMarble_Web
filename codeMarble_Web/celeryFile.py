from celery import Celery


app = Celery('tasks', broker='redis://localhost:6379')


@app.task(name='task.addProblem')
def addProblem(problemIndex, jsonData):
	pass


@app.task(name='task.compileCode')
def compileCode(codeIndex):
	pass


@app.task(name='task.matching')
def matching(problemIndex, challengerIndex, championIndex):
	pass
























