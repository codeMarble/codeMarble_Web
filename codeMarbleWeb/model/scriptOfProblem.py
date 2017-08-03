# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from codeMarbleWeb.model import Base

class ScriptOfProblem(Base):

    __tablename__ = 'ScriptOfProblem'

    problemIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= False,
                       nullable= False)

    userScript = Column(String,
                      unique= False)