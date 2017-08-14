# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, INTEGER, ENUM
from codeMarble_Web.model import Base

class User(Base):

    __tablename__ = 'User'

    userIndex = Column(INTEGER(unsigned=True),
                       primary_key=True,
                       autoincrement=True,
                       nullable=False)

    userId = Column(VARCHAR(20),
                    nullable=False,
                    unique=True)

    password = Column(CHAR(1024),
                      nullable=False,
                      unique=False)

    nickName = Column(VARCHAR(20),
                      nullable=False,
                      unique=True)

    eMail = Column(VARCHAR(256),
                   nullable=False,
                   unique=False)

    authority = Column(ENUM('admin', 'semiAdmin', 'user'),
                       nullable=False,
                       default='user')