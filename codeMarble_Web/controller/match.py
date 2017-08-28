# -*- coding: utf-8 -*-

import random
from flask import request, redirect, session, url_for, render_template, flash

from codeMarble_Web.database import dao
from codeMarble_Web.celeryFile import matching

from codeMarble_Web.codeMarble_blueprint import *

from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required
from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.utilUserInformationInProblem import get_total_score_each_users, get_topProblem
from codeMarble_Web.utils.utilUserSettingQuery import select_userSetting, get_user_information, update_userSetting
from codeMarble_Web.utils.utilLanguageQuery import select_language
from codeMarble_Web.utils.utilDataOfMatch import select_dataOfMatch
from codeMarble_Web.utils.utilProblemQuery import select_problem
from codeMarble_Web.utils.utilCodeQuery import select_code
from codeMarble_Web.utils.utilUserInformationInProblem import select_userInformationInProblem


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/match')
@login_required
@check_invalid_access
def match():
    try:
        userProblemSubquery = select_code(userIndex=session['userIndex']).group_by('problemIndex').subquery()
        problems = select_problem().subquery()
        userProblemList = dao.query(problems.c.problemName, userProblemSubquery.c.codeIndex,
                                    userProblemSubquery.c.problemIndex).\
                                join(userProblemSubquery,
                                     userProblemSubquery.c.problemIndex == problems.c.problemIndex).all()

        render_template('xxx.html',
                        userProblemList=userProblemList)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/match/list<int:problemIndex>')
@login_required
@check_invalid_access
def matchList(problemIndex):
    try:
        userIndex = session['userIndex']
        userScore = select_userInformationInProblem(userIndex=userIndex, problemIndex=problemIndex).first().score

        userListSubquery = select_code(problemIndex=problemIndex).group_by('userIndex').subquery()
        userProblemInfoSubquery = select_userInformationInProblem(problemIndex=problemIndex).subquery()
        userListSubquery = dao.query(userListSubquery.c.codeIndex, userListSubquery.c.userIndex,
                                     userListSubquery.c.problemIndex, userProblemInfoSubquery.c.score).\
                                join(userProblemInfoSubquery,
                                     userProblemInfoSubquery.c.problemIndex == userListSubquery.c.problemIndex).subquery()

        for i in range(50):
            userList_upper = dao.query(userListSubquery).filter(and_(userListSubquery.c.score < userScore + i*20,
                                                                     userListSubquery.c.score > userScore,
                                                                     userListSubquery.c.userIndex != userIndex)).all()

            if len(userList_upper) == 3:
                break

            elif len(userList_upper) > 3:
                while len(userList_upper) > 3:
                    userList_upper.remove(random.choice(list(userList_upper)))

                break

        for i in range(50):
            userList_lower = dao.query(userListSubquery).filter(and_(userListSubquery.c.score > userScore - i*20,
                                                                     userListSubquery.c.score <= userScore,
                                                                     userListSubquery.c.userIndex != userIndex)).all()

            if len(userList_lower) == 2:
                break

            elif len(userList_lower) > 2:
                while len(userList_lower) > 2:
                    userList_lower.remove(random.choice(list(userList_lower)))

                break

        return render_template('xxx.html',
                               userList_upper=userList_upper,
                               userList_lower=userList_lower)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/match/topList<int:problemIndex>')
@login_required
@check_invalid_access
def matchTopList(problemIndex):
    try:
        userListSubquery = select_code(problemIndex=problemIndex).group_by('userIndex').subquery()
        userProblemInfoSubquery = select_userInformationInProblem(problemIndex=problemIndex).subquery()
        topUserList = dao.query(userListSubquery.c.codeIndex, userListSubquery.c.userIndex,
                                userListSubquery.c.problemIndex, userProblemInfoSubquery.c.score).\
                            join(userProblemInfoSubquery,
                                 userProblemInfoSubquery.c.problemIndex == userListSubquery.c.problemIndex).\
                            order_by(userListSubquery.c.score.desc())[:3]

        return render_template('xxx.html',
                               topUserList=topUserList)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/match/matching<int:problemIndex><int:userIndex>')
@login_required
@check_invalid_access
def matching(problemIndex, userIndex):
    try:
        matching.delay(problemIndex, session['userIndex'], userIndex)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))































