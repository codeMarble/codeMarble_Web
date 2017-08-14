# -*- coding: utf-8 -*-

from flask import Blueprint

codeMarble = Blueprint('codeMarble_Web', __name__, template_folder='../templates', static_folder='../static')