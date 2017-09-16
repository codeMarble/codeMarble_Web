# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, INTEGER, BOOLEAN, TEXT
from codeMarble_Web.model import Base


class Problem(Base):

    __tablename__ = 'Problem'

    problemIndex = Column(INTEGER(unsigned=True),
                          primary_key=True,
                          autoincrement=True,
                          nullable=False)

    problemName = Column(VARCHAR(50),
                         unique=True,
                         nullable=False)

    placementRule = Column(CHAR(5),
                           nullable=False)

    placementOption = Column(CHAR(20),
                              unique= False)

    existRule = Column(CHAR(20),
                       nullable=False)

    existOption = Column(CHAR(20),
                             nullable=False)

    actionRule = Column(CHAR(5),
                        nullable=False)

    actionOption = Column(CHAR(20),
                           nullable=False)

    endingRule = Column(CHAR(5),
                        nullable=False)

    endingOption = Column(CHAR(20),
                          nullable=False)

    gameBoard = Column(TEXT,
                       nullable=False)

    dataBoard = Column(TEXT,
                       nullable=False)

    limitTime = Column(INTEGER(unsigned=True),
                       nullable=False)

    limitMemory = Column(INTEGER(unsigned=True),
                         nullable=False)

    level = Column(INTEGER(unsigned=True),
                   nullable=False)

    isDelete = Column(BOOLEAN,
                      unique=False)