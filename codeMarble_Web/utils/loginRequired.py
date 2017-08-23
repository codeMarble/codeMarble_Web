# -*- coding: utf-8 -*-

from flask import request, current_app, session, redirect, url_for, flash
from functools import wraps
from codeMarble_Web.resource.sessionResources import *


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_key = request.cookies.get(current_app.config['SESSION_COOKIE_NAME'])

            try:
                idx = session[USER_INDEX]

            except:
                idx = 0

            if not (session.sid == session_key and session.__contains__(USER_ID)):
                session.clear()

                flash('로그인 후 사용 가능한 메뉴입니다.')
                return redirect(url_for('.login'))

            return f(*args, **kwargs)

        except Exception:
            return "fbehdrl123"


    return decorated_function

