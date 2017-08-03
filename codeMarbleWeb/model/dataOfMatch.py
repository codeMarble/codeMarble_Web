# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from codeMarbleWeb.model import Base

class DataOfMatch(Base):

    __tablename__ = 'DataOfMatch'

    dataOfMatchIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= True,
                       nullable= False)

    problemIndex = Column(INTEGER(unsigned=True),
                       autoincrement=False,
                       nullable=False)

    challengerIndex = Column(INTEGER(unsigned=True),
                          autoincrement=False,
                          nullable=False)

    championIndex = Column(INTEGER(unsigned=True),
                             autoincrement=False,
                             nullable=False)

    result = Column(Enum('win', 'lose', 'draw', '...ing...', 'server error'),
                       default= '...ing...')

    positionData = Column(String,
                      unique= False)

    boardData = Column(String,
                      unique= False)