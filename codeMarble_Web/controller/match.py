# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template, flash

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *

from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.utilUserInformationInProblem import get_total_score_each_users, get_topProblem
from codeMarble_Web.utils.utilUserSettingQuery import select_userSetting, get_user_information, update_userSetting
from codeMarble_Web.utils.utilLanguageQuery import select_language
from codeMarble_Web.utils.utilDataOfMatch import select_dataOfMatch


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))

# @codeMarble.route()
# @check_invalid_access
# def temp():
#     pass