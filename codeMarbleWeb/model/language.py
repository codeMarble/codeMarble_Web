# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from model import Base

class Language(Base):

    __tablename__ = 'Language'

    LanguageIndex = Column(INTEGER(unsigned= True),
                           primary_key= True,
                           autoincrement= True,
                           nullable= False)

    language = Column(VARCHAR(20),
                      unique= False)