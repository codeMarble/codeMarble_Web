# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from codeMarble_Web.model import Base


class Problem(Base):

    __tablename__ = 'Problem'

    problemIndex = Column(INTEGER(unsigned=True),
                          primary_key=True,
                          autoincrement=True,
                          nullable=False)