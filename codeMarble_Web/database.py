# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker

class DBManager:

    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag = False, recycle_time=3600):
        DBManager.__engine = create_engine(db_url,
                                           pool_recycle=recycle_time,
                                           echo=db_log_flag)

        if not database_exists(DBManager.__engine.url):
            create_database(DBManager.__engine.url)

            DBManager.__engine = create_engine(db_url,
                                               pool_recycle=recycle_time,
                                               echo=db_log_flag)

        DBManager.__session = scoped_session(sessionmaker(autocommit=False,
                                                          autoflush=False,
                                                          bind=DBManager.__engine))

        global dao
        dao = DBManager.__session


    @staticmethod
    def init_db():
        from model import *
        from model import Base

        Base.metadata.create_all(bind=DBManager.__engine)

        try:
            from codeMarble_py3des import TripleDES
            from utils.utilUserQuery import insert_user
            from werkzeug.security import generate_password_hash
            from utils.utilUserSettingQuery import insert_userSetting
            from utils.utilProblemQuery import insert_problem
            from utils.utilLanguageQuery import insert_language

            print len(generate_password_hash(TripleDES.encrypt(str('user1'))))
            dao.add(insert_user(userId='master', password=generate_password_hash(TripleDES.encrypt(str('master'))),
                                nickName='master', eMail='aa', authority='admin'))

            dao.add(insert_user(userId='user1', password=generate_password_hash(TripleDES.encrypt(str('user1'))),
                                nickName='user1', eMail='bb'))
            dao.add(insert_userSetting(userIndex=2, languageIndex=1, thema='chrome', comment='TT'))

            dao.add(insert_language('C'))
            dao.add(insert_language('C++'))
            dao.add(insert_language('PYTHON2'))
            dao.add(insert_language('PYTHON3'))
            dao.add(insert_language('JAVA'))

            dao.commit()

        except Exception as e:
            print e
            dao.rollback()

dao = None