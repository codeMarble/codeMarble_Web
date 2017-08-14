# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN, TEXT
from codeMarble_Web.model import Base

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

    code = Column(TEXT,
                  unique=False)

    isOpen = Column(BOOLEAN,
                    unique= False)