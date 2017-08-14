# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarble_Web.model.user import User
from codeMarble_Web.model.board import Board
from codeMarble_Web.model.replyOfBoard import ReplyOfBoard

from codeMarble_Web.database import dao


def insert_board(userIndex, problemIndex, title, date, content):
    return Board(userIndex=userIndex,
                 problemIndex=problemIndex,
                 title=title,
                 content=content,
                 likeCount=0,
                 date=date,
                 isDelete=False)


def update_like_count(boardIndex, value):
    return dao.query(Board).\
                filter(Board.boardIndex == boardIndex).\
                update(dict(likeCount = Board.likeCount + value))


def insert_reply(boardIndex, userIndex, content):
    return ReplyOfBoard(boardIndex=boardIndex, userIndex=userIndex, content=content, isDelete=False)


def select_board_article(boardIndex=None):
    boardSubquery = dao.query(Board, User.userId, User.nickName).\
                        join(Board,
                             User.userIndex == Board.userIndex).\
                        filter(and_(Board.boardIndex == boardIndex if boardIndex
                                    else Board.boardIndex != boardIndex,
                                    Board.isDelete == False)).\
                        subquery()

    replySubquery = dao.query(ReplyOfBoard, User.userId, User.nickName).\
                        join(ReplyOfBoard,
                             User.userId == ReplyOfBoard.userIndex).\
                        filter(and_(ReplyOfBoard.boardIndex == boardIndex if boardIndex
                                    else ReplyOfBoard.boardIndex != boardIndex,
                                    ReplyOfBoard.isDelete == False)).\
                        subquery()

    return dao.query(boardSubquery, replySubquery.c.replyOfBoardIndex, replySubquery.c.userIndex.label('replyUserIndex'),
                     replySubquery.c.content.label('replyContent')).\
                join(boardSubquery,
                     replySubquery.c.boardIndex == boardSubquery.c.boardIndex)


def update_board_modify(boardIndex, problemIndex, title, content):
    dao.query(Board).\
        filter(Board.boardIndex==boardIndex).\
        update(dict(problemIndex=problemIndex,
                    title=title,
                    content=content))


def update_board_delete(boardIndex, isDelete=True):
    dao.query(Board).\
        filter(Board.boardIndex==boardIndex).\
        update(dict(isDelete=isDelete))


def update_reply_modify(boardIndex, content):
    dao.query(Board).\
        filter(Board.boardIndex==boardIndex).\
        update(dict(content=content))


def update_reply_delete(boardIndex, isDelete=True):
    dao.query(Board).\
        filter(Board.boardIndex==boardIndex).\
        update(dict(isDelete=isDelete))