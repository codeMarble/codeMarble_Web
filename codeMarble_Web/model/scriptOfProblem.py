# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT
from codeMarble_Web.model import Base

class ScriptOfProblem(Base):

    __tablename__ = 'ScriptOfProblem'

    problemIndex = Column(INTEGER(unsigned= True),
                          primary_key= True,
                          autoincrement= False,
                          nullable= False)

    userScript = Column(TEXT,
                        unique= False)