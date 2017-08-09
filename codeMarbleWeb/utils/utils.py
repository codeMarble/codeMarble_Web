# -*- coding: utf-8 -*-

from werkzeug.exceptions import BadRequest
from flask import session
from datetime import datetime

from codeMarbleWeb.utils import *
from codeMarbleWeb.resource.languageResources import *
from codeMarbleWeb.resource.routeResources import *
from codeMarbleWeb.resource.sessionResources import *
from codeMarbleWeb.resource.setResources import *

def get_is_check_request(form, name, checkOnValue, checkOffValue):
    try:
        form[name]
        return checkOffValue
    except BadRequest:
        return checkOffValue

def get_request_value(form, name):
    try:
        data = form[name]

        if type(data) != int:
            data = data.strip()
            data = data.replace('\r', '')

            if not len(data):
                raise Exception

        return data

    except (BadRequest, Exception):
        return None

def is_authority(authority):
    isServerAdministrator, isAdministrator, isUser = None, None, None

    try:
        if SERVER_ADMINISTRATOR in authority:
            isServerAdministrator = True
        if ADMINISTRATOR in authority or FREE_ADMINISTRATOR in authority:
            isAdministrator = True
        if USER in authority:
            isUser = True

        return (isServerAdministrator, isAdministrator, isUser)

    except Exception:
        return (None, None, None)

# def access_authority_check(userIndex = None, codeIndex = None,
#                            boardIndex = None, replyOfBoardIndex = None,
#                            languageIndex = None, userInformationInProblemUserIndex = None,
#                            userInformationInProblemProblemIndex=None, dataOfMatchIndex = None,
#                            scriptOfProblemProblemIndex = None, userSettingUserIndex = None,
#                            noticeIndex = None, isServerAdministrator = None):
#
#     try:
#         if userIndex == 0\
#             or codeIndex == 0\
#             or boardIndex == 0\
#             or replyOfBoardIndex == 0\
#             or languageIndex == 0\
#             or userInformationInProblemUserIndex == 0\
#             or userInformationInProblemProblemIndex == 0\
#             or dataOfMatchIndex == 0\
#             or scriptOfProblemProblemIndex == 0\
#             or userSettingUserIndex == 0\
#             or noticeIndex == 0:
#             return  False
#
#         authority = is_authority(session[USER_AUTHORITY])
#


