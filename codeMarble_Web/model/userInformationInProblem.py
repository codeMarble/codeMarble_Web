# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from codeMarble_Web.model import Base

class UserInformationInProblem(Base):

    __tablename__ = 'UserInformationInProblem'

    userIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= False,
                       nullable= False)
    problemIndex = Column(INTEGER(unsigned= True),
                          primary_key= True,
                          autoincrement= False,
                          nullable= False)

    score = Column(INTEGER(unsigned=True),
                           autoincrement=False,
                           nullable=False)