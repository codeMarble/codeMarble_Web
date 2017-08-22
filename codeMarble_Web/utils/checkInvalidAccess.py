# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, session, flash
from functools import wraps


def check_invalid_access(f):

	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			authority = session['authority']

			if 'admin' in request.endpoint and authority != 'admin':
				flash('접근 권한이 없는 계정입니다.')
				return redirect(url_for('.main'))

		except Exception as e:
			pass

		return f(*args, **kwargs)

	return decorated_function


	#     try:
	#         authority = session['authority']
	#
	#         print request.endpoint, '=========================='
	#
     #    except Exception as e:
	#         pass
	#
	# 	return f(*args, **kwargs)
	#
	# return decorated_function
