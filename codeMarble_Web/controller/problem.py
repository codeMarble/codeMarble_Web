# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template, flash
from datetime import datetime, date, timedelta

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *
from codeMarble_Web.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash


from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utilBoardQuery import *
from codeMarble_Web.utils.utilProblemQuery import select_problem
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.utilLanguageQuery import select_language
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required
from codeMarble_Web.utils.utilUserSettingQuery import select_userSetting
from codeMarble_Web.utils.utilCodeQuery import insert_code


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/problem/list', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def problemList():
    try:
        problemList = select_problem().all()
        print len(problemList), '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

        return render_template('list.html',
                               problemList=problemList)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/problem/problem<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def problem(problemIndex):
    try:
        userIndex = session['userIndex']
        problemData = select_problem(problemIndex=problemIndex).first()
        userInfo = select_userSetting(userIndex=userIndex)

        return render_template('gagagaga.html',
                               problemData=problemData,
                               userInfo=userInfo)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/problem/submit<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def submitProblem(problemIndex):
    try:
        isOpen = request.form['isOpen']
        language = request.form['language']
        languageIndex = select_language(language=language).first().languageIndex

        code = request.form[''] # .....



        insert_code(userIndex=session['userIndex'], problemIndex=problemIndex, languageIndex=languageIndex, code=code,
                    date=datetime.now(), isOpen=isOpen)

        dao.add()

        return redirect(url_for('.main'))   # ....

    except Exception as e:
        print e

        dao.rollback()

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))




















