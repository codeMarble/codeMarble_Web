# -*- coding: utf-8 -*-

from flask import request, redirect, session, url_for, render_template
from datetime import datetime, date, timedelta

from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *
from codeMarble_Web.codeMarble_py3des import TripleDES

from werkzeug.security import check_password_hash

from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utilBoardQuery import *
from codeMarble_Web.utils.utils import *
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/board', methods=['POST'])
@check_invalid_access
def board():
    if request.method == 'POST':
        articleQuery = select_board_article()
        articleSubquery = articleQuery.subquery()

        article = articleQuery.all()
        replyCount = dao.query(articleSubquery.c.boardIndex,
                               func.count(articleSubquery.c.boardIndex)).\
                         group.by(articleSubquery.c.boardIndex)

        return render_template('',
                               article=article,
                               replyCount=replyCount)


@codeMarble.route('/board/write<int:problemIndex>', methods=['POST'])
@check_invalid_access
def writeArticle(problemIndex):
    if request.method == 'POST':
        try:
            userIndex = session['userIndex']

            title = get_request_value(form=request.form,
                                      name='title')

            content = get_request_value(form=request.form,
                                        name='content')

            problemIndex = problemIndex

            dao.add(insert_board(userIndex=userIndex,
                                 problemIndex=problemIndex,
                                 title=title,
                                 date = datetime.now(),
                                 content=content))

            dao.commit()

        except Exception:
            dao.rollback()


@codeMarble.route('/board/delete<int:boardIndex>', methods=['POST'])
@check_invalid_access
def deleteArticle(boardIndex):
    if request.method == 'POST':
        try:
            articleIndex = select_board_article(boardIndex=boardIndex).first()

        except Exception:
            articleIndex = None

        update_board_delete(articleIndex, isDelete=True)

    try:
        dao.commit()

    except Exception:
        dao.rollback()


@codeMarble.route('/board/modify<int:boardIndex>', methods=['POST'])
@check_invalid_access
def modifyArticle(boardIndex):
    if request.method == 'POST':
        try:
            problemIndex = get_request_value(form=request.form,
                                             name='problemIndex')
            title = get_request_value(form=request.form,
                                      name='title')
            content = get_request_value(form=request.form,
                                        name='content')
            modifyIndex = select_board_article(boardIndex).first()

        except Exception:
            modifyIndex = None

        update_board_modify(modifyIndex, problemIndex=problemIndex,
                            title=title, content=content)

        try:
            dao.commit()

        except Exception:
            dao.rollback()


@codeMarble.route('/board/writeReply<int:boardIndex>', methods=['POST'])
@check_invalid_access
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


@codeMarble.route('/board/deleteReply<int:boardIndex>', methods=['POST'])
@check_invalid_access
def deleteReply(boardIndex):
    if request.method == 'POST':
        try:
            boardReply = select_board_article(boardIndex).first()

        except Exception:
            boardReply = None

        update_reply_delete(boardReply, isDelete=True)

    try:
        dao.commit()

    except Exception:
        dao.rollback()


@codeMarble.route('/board/modifyReply<int:boardIndex>', methods=['POST'])
@check_invalid_access
def modifyReply(boardIndex):
    if request.method == 'POST':
        try:
            modifyIndex = select_board_article(boardIndex).first()
            content = get_request_value(form=request.form,
                                        name='content')

        except Exception:
            modifyIndex = None

        update_reply_modify(modifyIndex, content=content)

    try:
        dao.commit()

    except Exception:
        dao.rollback()









