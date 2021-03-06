# -*- coding: utf-8 -*-

import time
from flask import request, redirect, session, url_for, render_template, flash

from codeMarble_Web.database import dao
from codeMarble_Web.celeryFile import compileCode

from codeMarble_Web.codeMarble_blueprint import *


from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utilBoardQuery import *
from codeMarble_Web.utils.utilProblemQuery import select_problem
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.utilLanguageQuery import select_language
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required
from codeMarble_Web.utils.utilUserSettingQuery import select_userSetting, insert_userSetting
from codeMarble_Web.utils.utilUserInformationInProblem import select_userInformationInProblem, insert_userInformationInProblem
from codeMarble_Web.utils.utilCodeQuery import insert_code, select_code, select_recent_code


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
    thema = ['chrome', 'clouds', 'eclipse', 'github', 'monokai', 'textmate', 'tomorrow']

    try:
        langQuery = select_language()
        userIndex = session['userIndex']
        problemData = select_problem(problemIndex=problemIndex).first()

        userInfoSub = select_userSetting(userIndex=userIndex).subquery()
        temp = langQuery.subquery()

        userInfo = dao.query(temp.c.language, userInfoSub).\
                        join(userInfoSub, userInfoSub.c.languageIndex == temp.c.languageIndex).first()

        language = langQuery.all()

        if userInfo is None:
            try:
                dao.add(insert_userSetting(userIndex=userIndex))
                dao.commit()

                redirect(url_for('.problem'))

            except Exception as e:
                redirect(url_for('.problem'))

        return render_template('problem.html',
                               problemData=problemData,
                               userInfo=userInfo,
                               thema=thema,
                               language=language)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/problem/submit<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def submitProblem(problemIndex):
    try:
        isOpen = True if request.form['isOpen'] == 't' else False
        language = request.form['language']
        languageIndex = select_language(language=language).first().languageIndex
        code = request.form['getCode']

        temp = select_userInformationInProblem(userIndex=session['userIndex'], problemIndex=problemIndex).first()

        if temp is None:
            dao.add_all([insert_code(userIndex=session['userIndex'], problemIndex=problemIndex,
                                    languageIndex=languageIndex, code=code, date=datetime.now(), isOpen=isOpen),
                        insert_userInformationInProblem(userIndex=session['userIndex'], problemIndex=problemIndex)])
        else:
            dao.add(insert_code(userIndex=session['userIndex'], problemIndex=problemIndex, languageIndex=languageIndex,
                                code=code, date=datetime.now(), isOpen=isOpen))

        dao.commit()

        compileCode.delay(codeIndex=select_code(userIndex=session['userIndex'], problemIndex=problemIndex).all()[-1].codeIndex)

        time.sleep(0.5)
        flash('정상적으로 제출됐습니다.')
        return redirect(url_for('.myCodeInProblem',
                                problemIndex=problemIndex))

    except Exception as e:
        print e

        dao.rollback()

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/problem/myCodeInProblem<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def myCodeInProblem(problemIndex):
    try:
        codeList = select_code(userIndex=session['userIndex'], problemIndex=problemIndex).all()
        problemName = select_problem(problemIndex=problemIndex).first().problemName

        return render_template('myCodeList_problem.html',
                               codeList=codeList,
                               problemIndex=problemIndex,
                               problemName=problemName)

    except Exception as e:
        print e
        dao.rollback()

        flash('다시 시도해주세요.')


@codeMarble.route('/problem/codeListInProblem<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def codeListInProblem(problemIndex):
    try:
        codeListSubquery = select_recent_code(problemIndex=problemIndex).subquery()
        codeListSubquery = dao.query(User.nickName, codeListSubquery).\
                                join(codeListSubquery,
                                     codeListSubquery.c.userIndex == User.userIndex).subquery()

        temp = select_code(problemIndex=problemIndex).subquery()
        codeListSubquery = dao.query(codeListSubquery, temp.c.isOpen).\
                                join(temp,
                                     temp.c.codeIndex == codeListSubquery.c.leastIndex).subquery()

        scoreListSuquery = select_userInformationInProblem(problemIndex=problemIndex).subquery()

        codeList = dao.query(scoreListSuquery.c.score, codeListSubquery).\
                        join(codeListSubquery,
                             codeListSubquery.c.userIndex == scoreListSuquery.c.userIndex).\
                        all()

        problemName = select_problem(problemIndex=problemIndex).first().problemName

        return render_template('codeList_problem.html',
                               codeList=codeList,
                               problemIndex=problemIndex,
                               problemName=problemName)

    except Exception as e:
        print e

        dao.rollback()

        flash('다시 시도해주세요.')


@codeMarble.route('/viewCode<int:codeIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def viewCode(codeIndex):
    tempCode = select_code(codeIndex=codeIndex).subquery()
    temp = select_language().subquery()

    code = dao.query(temp.c.language, tempCode).\
                join(tempCode,
                     tempCode.c.languageIndex == temp.c.languageIndex).first()

    userInfo = select_userInformationInProblem(userIndex=session['userIndex']).first()

    problem = select_problem(problemIndex=code.problemIndex).first()
    user = select_user(userIndex=session['userIndex']).first()

    return render_template('viewCode.html',
                           userInfo=userInfo,
                           code=code,
                           problem=problem,
                           user=user)















