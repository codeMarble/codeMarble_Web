# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker

class DBManager:

    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag = False, recycle_time = 3600):
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
            from werkzeug.security import generate_password_hash
            from utils.querys import insert_problem, insert_user
            from codeMarble_py3des import TripleDES

            dao.add(insert_problem('test1', 0, 2, 1, 1))
            dao.add(insert_problem('test2', 0, 2, 2, 1))
            dao.add(insert_problem('test3', 0, 1, 2, 1))
            dao.add(insert_user('master', 'master', generate_password_hash(TripleDES.encrypt(str('master')))))

            dao.commit()

        except Exception:
            dao.rollback()

dao = None