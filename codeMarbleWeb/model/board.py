# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from codeMarbleWeb.model import Base

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

    content = Column(String,
                      unique=False)

    likeCount = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)
