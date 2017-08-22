# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template
from datetime import datetime, date, timedelta

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *
from codeMarble_Web.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash


from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utilBoardQuery import *
from codeMarble_Web.utils.utilProblemQuery import select_problem
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/problem', methods=['GET', 'POST'])
@check_invalid_access
def problem():
    problemList = select_problem().all()
    print len(problemList), '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    return render_template('list.html',
                           problemList=problemList)


@codeMarble.route('/problemInfo<int:problemIndex>', methods=['GET', 'POST'])
@check_invalid_access
def problemInfo(problemIndex):
    print request.method
    problemData = select_problem(problemIndex=problemIndex).first()

    return render_template('gagagaga.html',
                           problemData=problemData)