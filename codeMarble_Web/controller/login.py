# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template
from datetime import datetime, date, timedelta

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *
from codeMarble_Web.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash

from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utilBoardQuery import *
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.utilUserInformationInProblem import get_total_score_each_users, get_topProblem
from codeMarble_Web.utils.utilUserSetting import *

from codeMarble_Web.resource.sessionResources import *
from codeMarble_Web.resource.htmlResource import *
from codeMarble_Web.resource.setResources import *
from codeMarble_Web.resource.routeResources import *


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


def check_user(request_form):
    try:
        userId = get_request_value(form=request.form, name='userId')
        password = get_request_value(form=request.form, name='password')

        user = select_user(userId=userId).first()

        if check_password_hash(user.password, TripleDES.encrypt(str(password))):
            session['userIndex'] = user.userIndex
            session['userId'] = user.userId
            session['nickName'] = user.nickName
            session['eMail'] = user.eMail
            session['authority'] = user.authority

            return True

        else:
            return 'wrong id or password'

    except Exception as e:
        return 'wrong id or password'




@codeMarble.route('/', methods=['GET', 'POST'])
def main():
    topUsers = get_total_score_each_users().all()
    topProblems = get_topProblem().all()

    return render_template('main.html',
                           topUsers=topUsers[:3] if len(topUsers) < 3 else topUsers,
                           topProblems=topProblems[:3] if len(topProblems) < 3 else topProblems)


@codeMarble.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if check_user(request.form) is True:
            topUsers = get_total_score_each_users().all()
            topProblems = get_topProblem().all

            return render_template('main.html',
                                   topUsers=topUsers[:3],
                                   topProblems=topProblems[:3])

        else:
            return '.....'

    else:
        return render_template('login.html')


@codeMarble.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass

    else:
        return render_template('xxx.html')


@codeMarble.route('/setting', methods=['POST'])
def setting():
    try:
        userInformation = select_userSetting(userIndex=session['userIndex']).first()

    except Exception:
        userInformation = ''


    return render_template('setting.html',
                           userInformation=userInformation)


@codeMarble.route('/saveSetting', methods=['POST'])
def saveSetting():
    if request.method == 'POST':
        # nickName = get_request_value(form=request.form,
        #                              name='nickName')

        languageIndex = get_request_value(form=request.form,
                                          name='languageIndex')

        thema = get_request_value(form=request.form,
                                  name='thema')

        comment = get_request_value(form=request.form,
                                    name='comment')

        isOpen = get_request_value(form=request.form,
                                   name='isOpen')


        update_userSetting(select_userSetting(userIndex=session['userIndex']).first(),
                           languageIndex,
                           thema,
                           comment,
                           isOpen)

        try:
            dao.commit()

            return redirect(url_for('.signin'))

        except Exception:
            dao.rollback()
            error = 'error'

    return render_template('setting.html',
                           languageIndex,
                           thema,
                           comment,
                           isOpen,
                           error)