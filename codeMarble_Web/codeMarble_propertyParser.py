import os
from runServer import thisPath


configs = {'DBuser': 'root',
           'DBpassword': '',
           'DBIP': 'localhost',
           'redisIP': 'localhost',
           'redisPort': 6379,
           'webPort': 9410,
           'processCount': 2}

def propertyParser():
	with open(os.path.join(thisPath, 'codeMarble.properties')) as fp:
	    lines = fp.readlines()

	    for line in lines:
	        pos = line.find('#')

	        if pos > 0:
	            line = line[:pos]

	            if len(line) > 1:
	                name, setting = [i.strip() for i in line.split('=')]
	                configs[name] = setting