# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from model import Base

class Code(Base):

    __tablename__ = 'Code'

    codeIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= True,
                       nullable= False)

    userIndex = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    problemIndex = Column(INTEGER(unsigned= True),
                          autoincrement= False,
                          nullable= False)

    languageIndex = Column(INTEGER(unsigned= True),
                           autoincrement= False,
                           nullable= False)

    code = Column(String,
                  unique=False)

    isOpen = Column(Boolean,
                    unique= False)