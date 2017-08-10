# -*- coding: utf-8 -*-

from sqlalchemy import *

from codeMarbleWeb.model.user import User
from codeMarbleWeb.model.board import Board
from codeMarbleWeb.model.replyOfBoard import ReplyOfBoard

from codeMarbleWeb.database import dao


def insert_board(userIndex, problemIndex, title, content):
    return Board(userIndex=userIndex, problemIndex=problemIndex,
                 title=title, content=content, likeCount=0, isDelete=False)

def update_like_count(boardIndex, value):
    return dao.query(Board).\
                filter(Board.boardIndex == boardIndex).\
                update(dict(likeCount = Board.likeCount + value))

def insert_reply(boardIndex, userIndex, content):
    return ReplyOfBoard(boardIndex=boardIndex, userIndex=userIndex, content=content)

def select_board_article(boardIndex):
    boardSubquery = dao.query(Board, User.userId, User.nickName).\
                        join(Board,
                             User.userIndex == Board.userIndex).\
                        filter(Board.boardIndex == boardIndex).subquery()

    replySubquery = dao.query(ReplyOfBoard, User.userId, User.nickName).\
                        join(ReplyOfBoard,
                             User.userId == ReplyOfBoard.userIndex).\
                        filter(ReplyOfBoard.boardIndex == boardIndex).subquery()

    return dao.query(boardSubquery, replySubquery.c.replyOfBoardIndex,
                      replySubquery.c.userIndex.label('replyUserIndex'), replySubquery.c.content.label('replyContent')).\
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