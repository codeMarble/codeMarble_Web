# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN, ENUM
from codeMarble_Web.model import Base

class UserSetting(Base):

    __tablename__ = 'UserSetting'

    userIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= False,
                       nullable= False)

    languageIndex = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    thema = Column(ENUM('chorme', 'clouds', 'eclipse', 'github', 'monokai', 'textmate', 'tomorrow'),
                       default= 'chorme')

    comment = Column(VARCHAR(80),
                      unique= True)

    isOpen = Column(BOOLEAN,
                    unique= False)