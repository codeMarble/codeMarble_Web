# # -*- coding: utf-8 -*-
#
# from flask import request, redirect, url_for, session
# from functools import wraps
# from repoze.lru import lru_cache
#
# from resource.sessionResources import *
# from resource.routeResources import *
# from utils import *
#
# from __builtin__ import True
#
# @lru_cache(maxsize=300)
# def check_invalid_access(f):
#
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         try:
#             userIndex = get_request_value
