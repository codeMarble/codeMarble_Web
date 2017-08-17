# -*- coding: utf-8 -*-

from werkzeug.exceptions import BadRequest
from flask import session
from datetime import datetime

from codeMarble_Web.utils import *
from codeMarble_Web.resource.languageResources import *
from codeMarble_Web.resource.routeResources import *
from codeMarble_Web.resource.sessionResources import *
from codeMarble_Web.resource.setResources import *

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