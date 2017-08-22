# -*- coding: utf-8 -*-

from flask import *
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

                return redirect(url_for('.login'))

            return f(*args, **kwargs)

        except Exception:
            return "fbehdrl123"


    return decorated_function

