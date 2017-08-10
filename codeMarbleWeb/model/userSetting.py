# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from codeMarbleWeb.model import Base

class UserSetting(Base):

    __tablename__ = 'UserSetting'

    userIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= False,
                       nullable= False)

    languageIndex = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    thema = Column(Enum('chorme', 'clouds', 'eclipse', 'github', 'monokai', 'textmate', 'tomorrow'),
                       default= 'chorme')

    comment = Column(VARCHAR(80),
                      unique= True)

    isOpen = Column(Boolean,
                    unique= False)