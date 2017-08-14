# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT, ENUM
from codeMarble_Web.model import Base

class User(Base):

    __tablename__ = 'User'

    userIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= True,
                       nullable= False)

    userId = Column(VARCHAR(30),
                    nullable= False,
                    unique= True)

    password = Column(TEXT,
                      unique= False)

    nickName = Column(VARCHAR(70),
                      unique= True)

    eMail = Column(VARCHAR(70),
                   unique= False)

    authority = Column(ENUM('admin', 'semiAdmin', 'user'),
                       default= 'user')