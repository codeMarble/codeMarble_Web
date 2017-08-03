# -*- coding: utf-8 -*-

from flask import *
from functools import wraps
from repoze.lru import lru_cache
from resource.sessionResources import *
from resource.routeResources import *
from codeMarble_blueprint import codeMarble

@lru_cache(maxsize=300)
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

                return redirect(url_for(SIGN_IN_NEWPAGE, inIdx=idx, to=f.__name__, params=kwargs))

            return f(*args, **kwargs)

        except Exception:
            return "fbehdrl123"


    return decorated_function

