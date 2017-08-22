# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template, flash
from datetime import datetime, date, timedelta

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *
from codeMarble_Web.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash, generate_password_hash

from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.utilUserInformationInProblem import get_total_score_each_users, get_topProblem
from codeMarble_Web.utils.utilUserSettingQuery import select_userSetting, get_user_information, update_userSetting
from codeMarble_Web.utils.utilLanguageQuery import select_language


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


def check_user(request_form):
    try:
        userId = get_request_value(form=request_form, name='userId')
        password = get_request_value(form=request_form, name='password')

        user = select_user(userId=userId).first()

        print user.password

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

    try:
        user = select_user(userIndex=session['userIndex'])
        return render_template('main.html',
                               topUsers=topUsers[:3] if len(topUsers) < 3 else topUsers,
                               topProblems=topProblems[:3] if len(topProblems) < 3 else topProblems,
                               user=user)

    except Exception as e:
        return render_template('main.html',
                               topUsers=topUsers[:3] if len(topUsers) < 3 else topUsers,
                               topProblems=topProblems[:3] if len(topProblems) < 3 else topProblems,
                               user=None)


@codeMarble.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            message = check_user(request.form)
            if message is True:
                return redirect(url_for('.main'))

            else:
                flash(message)
                return render_template('login.html')

        else:
            return render_template('login.html')

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


@codeMarble.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass

    else:
        return render_template('xxx.html')


@codeMarble.route('/setting', methods=['GET', 'POST'])
@check_invalid_access
def setting():
    thema = ['chrome', 'clouds', 'eclipse', 'github', 'monokai', 'textmate', 'tomorrow']
    try:
        userInformation = get_user_information(session['userIndex']).first()
        language = select_language().all()

    except Exception as e:
        print e

        flash('다시 시도해주세요.')
        return redirect(url_for('.main'))


    return render_template('setting.html',
                           userInformation=userInformation,
                           language=language,
                           thema=thema)


@codeMarble.route('/saveSetting', methods=['POST'])
@check_invalid_access
def saveSetting():
    nickName = get_request_value(request.form, 'nickName')
    password = get_request_value(request.form, 'pw')
    password = generate_password_hash(TripleDES.encrypt(str(password))) if password else None
    eMail = get_request_value(request.form, 'eMail')

    comment = get_request_value(request.form, 'comment')
    isOpen = True if get_request_value(request.form, 'optionsRadios1') else False
    language = get_request_value(request.form, 'language')
    thema = get_request_value(request.form, 'thema')

    languageIndex = select_language(language=language).first().languageIndex

    try:
        update_userSetting(userIndex=session['userIndex'], languageIndex=languageIndex, thema=thema,
                           comment=comment, isOpen=isOpen)
        update_user(userIndex=session['userIndex'], password=password,
                    nickName=nickName, eMail=eMail)

        dao.commit()

    except Exception as e:
        dao.rollback()

        flash('정보변경에 실패했습니다.')
        return redirect(url_for('.main'))

    flash('정상적으로 정보가 변경되었습니다.')
    return redirect(url_for('.main'))


@codeMarble.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')