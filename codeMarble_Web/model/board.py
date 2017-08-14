# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT, BOOLEAN
from codeMarble_Web.model import Base

class Board(Base):

    __tablename__ = 'Board'

    boardIndex = Column(INTEGER(unsigned= True),
                        primary_key= True,
                        autoincrement= True,
                        nullable= False)

    userIndex = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    problemIndex = Column(INTEGER(unsigned= True),
                          autoincrement= False,
                          nullable= False)

    title = Column(VARCHAR(80),
                   unique= False)

    content = Column(TEXT,
                      unique=False)

    likeCount = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    isDelete = Column(BOOLEAN,
                      unique=False)