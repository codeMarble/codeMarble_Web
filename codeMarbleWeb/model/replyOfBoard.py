# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from model import Base

class ReplyOfBoard(Base):

    __tablename__ = 'ReplyOfBoard'

    replyOfBoardIndex = Column(INTEGER(unsigned= True),
                               primary_key= True,
                               autoincrement= True,
                               nullable= False)

    boardIndex = Column(INTEGER(unsigned= True),
                        autoincrement= False,
                        nullable= False)

    userIndex = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    content = Column(VARCHAR(150),
                     unique= False)