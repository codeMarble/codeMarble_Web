# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN
from codeMarble_Web.model import Base

class Notice(Base):

    __tablename__ = 'Notice'

    noticeIndex = Column(INTEGER(unsigned= True),
                       primary_key= True,
                       autoincrement= False,
                       nullable= False)

    userIndex = Column(INTEGER(unsigned= True),
                       autoincrement= False,
                       nullable= False)

    content = Column(VARCHAR(80),
                      unique= True)

    isRead = Column(BOOLEAN,
                    unique= False)