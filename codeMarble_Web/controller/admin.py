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
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required

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


@codeMarble.route('/admin', methods=['GET', 'POST'])
@check_invalid_access
def admin():
    return 'temp'


@codeMarble.route('/admin/enterSubAdmin<int:userIndex>', methods=['POST'])
@login_required
@check_invalid_access
def enterSubAdmin(userIndex):
    if request.method == 'POST':
        password = get_request_value(form=request.form,
                                     name='password')

        nickName = get_request_value(form=request.form,
                                     name='nickName')

        eMail = get_request_value(form=request.form,
                                  name='eMail')

        update_user(userIndex, password=password, nickName=nickName,
                    eMail=eMail, authority='semiAdmin')

        try:
            dao.commit()

        except Exception:
            dao.rollback() 


@codeMarble.route('/admin/deleteSubAdmin<int:userIndex>', methods=['POST'])
@login_required
@check_invalid_access
def deleteSubAdmin(userIndex):
    if request.method == 'POST':
        password = get_request_value(form=request.form,
                                     name='password')

        nickName = get_request_value(form=request.form,
                                     name='nickName')

        eMail = get_request_value(form=request.form,
                                  name='eMail')

        update_user(userIndex, password=password, nickName=nickName,
                    eMail=eMail, authority='user')

        try:
            dao.commit()

        except Exception:
            dao.rollback()





