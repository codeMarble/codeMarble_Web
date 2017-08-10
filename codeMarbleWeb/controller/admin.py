# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template
from datetime import datetime, date, timedelta

from codeMarbleWeb.database import dao

from codeMarbleWeb.codeMarble_blueprint import *
from codeMarbleWeb.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash

from codeMarbleWeb.utils.utilUserQuery import *
from codeMarbleWeb.utils.utilBoardQuery import *
from codeMarbleWeb.utils.utils import *

from codeMarbleWeb.resource.sessionResources import *
from codeMarbleWeb.resource.htmlResource import *
from codeMarbleWeb.resource.setResources import *
from codeMarbleWeb.resource.routeResources import *

@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarbleWeb.codeMarble_logger import *
        Log.error(str(e))



@codeMarble.route('/admin/enterSubAdmin<int:userIndex>', methods=['POST'])
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





