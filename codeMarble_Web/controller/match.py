# -*- coding: utf-8 -*-

import random
import datetime

from flask import redirect, url_for, render_template, flash

from codeMarble_Web.celeryFile import matching
from codeMarble_Web.codeMarble_blueprint import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required
from codeMarble_Web.utils.utilCodeQuery import select_code
from codeMarble_Web.utils.utilProblemQuery import select_problem
from codeMarble_Web.utils.utilUserInformationInProblem import select_userInformationInProblem
from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utils import *


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/match', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def matchProblemList():
    try:
        userProblemSubquery = select_code(userIndex=session['userIndex'], isCompile=True).group_by('problemIndex').subquery()
        problems = select_problem().subquery()
        userProblemList = dao.query(problems.c.problemName, userProblemSubquery.c.codeIndex,
                                    userProblemSubquery.c.problemIndex).\
                                join(userProblemSubquery,
                                     userProblemSubquery.c.problemIndex == problems.c.problemIndex).all()

        return render_template('matchProblemList.html',
                               userProblemList=userProblemList)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/match/userList<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def matchUserList(problemIndex):
    try:
        userIndex = session['userIndex']
        userScore = select_userInformationInProblem(userIndex=userIndex, problemIndex=problemIndex).first().score

        userListSubquery = select_code(problemIndex=problemIndex, isCompile=True).group_by('userIndex').subquery()
        userProblemInfoSubquery = select_userInformationInProblem(problemIndex=problemIndex).subquery()
        userListSubquery = dao.query(userListSubquery.c.codeIndex, userListSubquery.c.userIndex,
                                     userListSubquery.c.problemIndex, userProblemInfoSubquery.c.score).\
                                join(userProblemInfoSubquery,
                                     userProblemInfoSubquery.c.userIndex == userListSubquery.c.userIndex).subquery()

        for i in range(50):
            userList_upper_subquery = dao.query(userListSubquery).\
                                        filter(and_(userListSubquery.c.score < userScore + i*20,
                                                    userListSubquery.c.score > userScore,
                                                    userListSubquery.c.userIndex != userIndex)).subquery()

            userList_upper = dao.query(User.nickName, userList_upper_subquery). \
                                join(userList_upper_subquery,
                                     userList_upper_subquery.c.userIndex == User.userIndex). \
                                all()

            if len(userList_upper) == 3:
                break

            elif len(userList_upper) > 3:
                while len(userList_upper) > 3:
                    userList_upper.remove(random.choice(list(userList_upper)))

                break

        for i in range(50):
            userList_lower_subquery = dao.query(userListSubquery).\
                                        filter(and_(userListSubquery.c.score > userScore - i*20,
                                                    userListSubquery.c.score <= userScore,
                                                    userListSubquery.c.userIndex != userIndex)).subquery()

            userList_lower = dao.query(User.nickName, userList_lower_subquery).\
                                join(userList_lower_subquery,
                                     userList_lower_subquery.c.userIndex == User.userIndex).\
                                all()

            if len(userList_lower) == 2:
                break

            elif len(userList_lower) > 2:
                while len(userList_lower) > 2:
                    userList_lower.remove(random.choice(list(userList_lower)))

                break

        problem = select_problem(problemIndex=problemIndex).first()

        return render_template('matchUserList.html',
                               userList_upper=userList_upper,
                               userList_lower=userList_lower,
                               problem=problem,
                               score=userScore)

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/match/rank<int:problemIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def matchRank(problemIndex):
    try:
        userListSubquery = select_code(problemIndex=problemIndex, isCompile=True).group_by('userIndex').subquery()
        userProblemInfoSubquery = select_userInformationInProblem(problemIndex=problemIndex).subquery()

        topUserListSubquery = dao.query(userListSubquery.c.codeIndex, userListSubquery.c.userIndex,
                                        userListSubquery.c.problemIndex, userProblemInfoSubquery.c.score).\
                                join(userProblemInfoSubquery,
                                     userProblemInfoSubquery.c.userIndex == userListSubquery.c.userIndex).\
                                order_by(userProblemInfoSubquery.c.score.desc()).\
                                subquery()

        topUserList = dao.query(User.nickName, topUserListSubquery).\
                        join(topUserListSubquery,
                             topUserListSubquery.c.userIndex == User.userIndex).all()

        problem = select_problem(problemIndex=problemIndex).first()

        topUserList = topUserList if len(topUserList) < 10 else topUserList[:10]

        return render_template('userRankInProblem.html',
                               topUserList=topUserList,
                               problem=problem)

    except Exception as e:
        print e, '!!!!!!!!!!!!!!!!!'

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/match/matching<int:problemIndex><int:userIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def matching(problemIndex, userIndex):
    try:
        matching.delay(problemIndex, session['userIndex'], userIndex)

        update_user(lastMatchDate=datetime.datetime.now())
        dao.commit()

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))































