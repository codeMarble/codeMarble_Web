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

    placementRule = Column(INTEGER(unsigned=True),
                           nullable=False)

    placementOption1 = Column(INTEGER(unsigned=True),
                              nullable=False)

    placementOption2 = Column(TEXT,
                              unique= False)

    existRule = Column(CHAR(8),
                       nullable=False)

    existOption = Column(CHAR(8),
                             nullable=False)

    actionRule = Column(INTEGER(unsigned=True),
                        nullable=False)

    actionOption1 = Column(INTEGER(unsigned=True),
                           nullable=False)

    actionOption2 = Column(INTEGER(unsigned=True),
                           nullable=False)

    endingRule = Column(INTEGER(unsigned=True),
                        nullable=False)

    endingOption = Column(CHAR(5),
                          nullable=False)

    limitTime = Column(INTEGER(unsigned=True),
                       nullable=False)

    limitMemory = Column(INTEGER(unsigned=True),
                         nullable=False)

    level = Column(INTEGER(unsigned=True),
                   nullable=False)

    isDelete = Column(BOOLEAN,
                      unique=False)