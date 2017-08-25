import os
import json
from celery import Celery


dataDir = os.path.join(os.getcwd(), 'problemData')
os.mkdir(dataDir)
app = Celery('tasks', broker='redis://localhost:6379')


@app.task(name='task.addProblem')
def addProblem(jsonData, problemIndex):
	with open(os.path.join(dataDir,"%i.json"%problemIndex), 'w', encoding='utf-8') as fp:
		json.dump(jsonData, fp)


@app.task(name='task.matching')
def matching(problemIndex, challengerIndex, championIndex):
	pass