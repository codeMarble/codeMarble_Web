# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template, flash

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *

from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required
from codeMarble_Web.utils.utilUserInformationInProblem import get_total_score_each_users, get_topProblem
from codeMarble_Web.utils.utilUserSettingQuery import select_userSetting, get_user_information, update_userSetting
from codeMarble_Web.utils.utilLanguageQuery import select_language
from codeMarble_Web.utils.utilProblemQuery import select_problem
from codeMarble_Web.utils.utilDataOfMatch import select_dataOfMatch


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/replay/myList', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def replayMyList():
	try:
		user = select_user(userIndex=session['userIndex']).subquery()
		problem = select_problem().subquery()
		totalUser = select_user().subquery()

		try:
			# if user is challenger
			replayData_challenge = select_dataOfMatch(challengerIndex=session['userIndex']).subquery()
			joinedquery_challenge = dao.query(user.c.nickName.label('challengerNickName'), user.c.userId.label('challengerId'),
			                        replayData_challenge.c.dataOfMatchIndex, replayData_challenge.c.problemIndex,
			                        replayData_challenge.c.challengerIndex, replayData_challenge.c.championIndex,
			                        replayData_challenge.c.result).\
								join(replayData_challenge,
			                         replayData_challenge.c.challengerIndex == user.c.userIndex).\
								subquery()

			userReplayData_challenge = dao.query(totalUser.c.nickName.label('championNickName'),
			                                     totalUser.c.userId.label('championId'),
			                                     joinedquery_challenge).\
											join(joinedquery_challenge,
			                                     joinedquery_challenge.c.championIndex == totalUser.c.userIndex).\
											subquery()

		except AttributeError as e:
			userReplayData_challenge = []

		try:
			# if user is champion
			replayData_champ = select_dataOfMatch(chapionIndex=session['userIndex']).subquery()
			joinedquery_champ = dao.query(user.c.nickName.label('championNickName'), user.c.userId.label('championId'),
			                              replayData_champ.c.dataOfMatchIndex, replayData_champ.c.problemIndex,
			                              replayData_champ.c.challengerIndex, replayData_champ.c.championIndex, replayData_champ.c.result). \
									join(replayData_champ,
			                             replayData_champ.c.championIndex == user.c.userIndex).\
									subquery()

			userReplayData_champ = dao.query(totalUser.c.nickName.label('challengerNickName'),
			                           totalUser.c.userId.label('challengerId'), joinedquery_champ).\
								join(joinedquery_champ,
			                         joinedquery_champ.c.championIndex == totalUser.c.userIndex).\
								subquery()

		except AttributeError as e:
			userReplayData_champ = []


		userReplayData_challenge = dao.query(problem.c.problemName, userReplayData_challenge).\
										join(userReplayData_challenge,
		                                     userReplayData_challenge.c.problemIndex == problem.c.problemIndex).all()

		userReplayData_champ = dao.query(problem.c.problemName, userReplayData_champ).\
									join(userReplayData_champ,
		                                 userReplayData_champ.c.problemIndex == problem.c.problemIndex).all()

		return render_template('replaymylist.html',
		                       userReplayData_challenge=userReplayData_challenge,
		                       userReplayData_champ=userReplayData_champ)

	except Exception as e:
		print e, type(e)

		flash('다시 시도해주세요.')
		return redirect(url_for('.main'))


@codeMarble.route('/replay/allList', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def allList():
	try:
		problem = select_problem().subquery()
		totalUser = select_user().subquery()

		replayData = select_dataOfMatch(challengerIndex=session['userIndex']).subquery()
		joinedquery = dao.query(totalUser.c.nickName.label('challengerNickName'), totalUser.c.userId.label('challengerId'),
		                        replayData.c.dataOfMatchIndex, replayData.c.problemIndex,
		                        replayData.c.challengerIndex, replayData.c.championIndex, replayData.c.result). \
						join(replayData,
		                     replayData.c.challengerIndex == totalUser.c.userIndex). \
						subquery()

		userReplayData = dao.query(totalUser.c.nickName.label('championNickName'), totalUser.c.userId.label('championId'),
		                           joinedquery). \
							join(joinedquery,
		                         joinedquery.c.championIndex == totalUser.c.userIndex). \
							subquery()

		userReplayData = dao.query(problem.c.problemName, userReplayData). \
							join(userReplayData,
		                         userReplayData.c.problemIndex == problem.c.problemIndex).all()

		return render_template('replaylist.html',
		                       userReplayData=userReplayData)

	except AttributeError as e:
		print e

		return render_template('replaylist.html',
		                       userReplayData=[])

	except Exception as e:
		flash('다시 시도해주세요.')
		return redirect(url_for('.main'))


@codeMarble.route('/replay/playResult<int:dataOfMatchIndex>', methods=['GET', 'POST'])
@login_required
@check_invalid_access
def playResult(dataOfMatchIndex):
	try:
		replayData = select_dataOfMatch(dataOfMatchIndex=dataOfMatchIndex).first()

		return render_template('xxx.html',
		                       replayData=replayData)

	except Exception as e:
		flash('다시 시도해주세요.')
		return redirect(url_for('.main'))


























