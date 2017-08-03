# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from model import Base

class User(Base):

    __tablename__ = 'User'

    userIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= True,
                       nullable= False)

    userId = Column(VARCHAR(30),
                    nullable= False,
                    unique= True)

    password = Column(String,
                      unique= False)

    nickName = Column(VARCHAR(70),
                      unique= True)

    eMail = Column(VARCHAR(70),
                   unique= False)

    authority = Column(Enum('admin', 'semiAdmin', 'user'),
                       default= 'user')