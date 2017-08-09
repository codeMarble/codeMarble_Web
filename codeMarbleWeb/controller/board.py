# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template
from datetime import datetime, date, timedelta

from codeMarbleWeb.database import dao

from codeMarbleWeb.codeMarble_blueprint import *
from codeMarbleWeb.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash

from codeMarbleWeb.utils.utilUserQuery import *
from codeMarbleWeb.utils.utilBoardQuery import *
from codeMarbleWeb.utils.utils import *

from codeMarbleWeb.resource.sessionResources import *
from codeMarbleWeb.resource.htmlResource import *
from codeMarbleWeb.resource.setResources import *
from codeMarbleWeb.resource.routeResources import *

@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarbleWeb.codeMarble_logger import *
        Log.error(str(e))



# @codeMarble.route('/board', methods=['GET', 'POST'])
# def board():
#     if request.method == 'POST':
#         article =



@codeMarble.route('/board/write<int:problemIndex>', methods=['POST'])
def writeArticle(problemIndex):
    if request.method == 'POST':
        userIndex = get_request_value(form=request.form,
                                      name='userIndex')

        title = get_request_value(form=request.form,
                                  name='title')

        content = get_request_value(form=request.form,
                                    name='content')

        dao.add(insert_board(userIndex=userIndex, problemIndex=problemIndex,
                             title=title, content=content))

        try:
            dao.commit()

        except Exception:
            dao.rollback()


@codeMarble.route('board/writeReply<int:boardIndex>', methods=['POST'])
def writeReply(boardIndex):
    if request.method == 'POST':
        userIndex = get_request_value(form=request.form,
                                      name='userIndex')

        content = get_request_value(form=request.form,
                                    name='content')


        dao.add(insert_reply(boardIndex=boardIndex, userIndex=userIndex,
                             content=content))

    try:
        dao.commit()

    except Exception:
        dao.rollback()


# @codeMarble.route('board/deleteReply<int:boardIndex>', methods=['POST'])
# def deleteReply(boardIndex):
#     if request.method == 'POST':
#         try:
#             boardReply = select_board_article(boardIndex=session['boardIndex'])










