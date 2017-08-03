# -*- coding: utf-8 -*-

from sqlalchemy import *

from resource.enumResource import *
from resource.setResources import *
from resource.otherResource import *
from resource.languageResources import *

from model.board import *
from model.replyOfBoard import *

from database import dao

def insert_articles_on_board(problemIndex, memberParameter, articleType, articleParameter):
    return Board(problemIndex = problemIndex,
                 )