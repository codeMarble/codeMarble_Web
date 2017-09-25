# -*- coding: utf-8 -*-
"""
    codeMarble_Core.actionRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    check and manage rule after placement rule.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys

from errorCode import *


class ActionRule(object):
    def __init__(self):
        pass

    # actionRuleNum(0:script, 1:remove, 2:change), actionRuleOption1(0:script, 1:＋dir, 2:×dir, 3:8dir, 4:go)
    # actionRuleOption2(0:othello, n:size)
    def checkActionRule(self, data):
        try:
            if data.actionRule is 1:
                return self.removeObject(data)

            elif data.actionRule is 2:
                return self.changeObject(data)

            else:
                return SERVER_ERROR

        except Exception as e:
            return SERVER_ERROR

    # actionRuleOption1(0:script, 1:＋dir, 2:×dir, 3:8dir, 4:go)
    # actionRuleOption2(0:othello, n:size)
    # actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos
    def removeObject(self, data):
        try:
            if 1 <= data.actionOption[0] <= 3: # remove size or othello
                if data.actionOption[1] == 0: # othello
                    return self.actionObjectByOthello(data.gameBoard, data.pos, 0)

                else: # size
                    return self.actionObjectBySize(data.gameBoard, data.pos, data.actionOption, 0)

            elif data.actionOption[0] == 4:  # remove go rule
                return self.actionObjectByGo(data.gameBoard, data.pos, 0)

            else:
                return SERVER_ERROR

        except Exception as e:
            return SERVER_ERROR

    def actionObjectByGo(self, board, pos, value):
        pi, pj = pos
        me = board[pi][pj]
        you = -me

        goRule = self.GoRule()

        yous = goRule.findYou(board, pos)
        for (i, j) in yous:
            if goRule.checkBoard(board, (i, j)):
                goRule.remove(board, (i, j), value)

        return True

    def actionObjectBySize(self, board, pos, actionOption, value):
        pi, pj = pos
        directions = self.getDirection(actionOption[0])

        for i in range(1, actionOption[1] + 1):
            for d in directions:
                try:
                    if ((0 <= pi + d[0] * i < len(board)) and (0 <= pj + d[1] * i < len(board))) and board[pi + d[0] * i][pj + d[1] * i] < 0:
                        board[pi + d[0] * i][pj + d[1] * i] *= -1
                except Exception as e:
                    continue

        return True

    def actionObjectByOthello(self, board, pos, value):
        pi, pj = pos
        dirs = self.getDirection(1)
        me = board[pi][pj]
        you = -me

        for d in dirs:
            for i in range(len(board)):
                try:
                    ni, nj = pi + i * d[0], pj + i * d[1]
                    if board[ni][nj] == me:
                        i, j = pi, pj
                        while i+d[0] != ni or j+d[1] != nj:
                            board[i+d[0]][j+d[1]] = value
                            i, j = i + d[0], j + d[1]
                        break

                except Exception as e:
                    break

        return True

    def getDirection(self, actionRuleOption):
        if actionRuleOption is 1:
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]

        elif actionRuleOption is 2:
            dirs = [[-1, -1], [-1, 1], [1, -1], [1, 1]]

        elif actionRuleOption is 3:
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, -1], [-1, 1], [1, -1], [1, 1]]

        else:
            return SERVER_ERROR

        return dirs

    # actionRuleNum, actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos
    def changeObject(self, data):
        try:
            if 1 <= data.actionOption[0] <= 3:  # if direction
                if data.actionOption[1] == 0:  # by othello
                    return self.actionObjectByOthello(data.gameBoard, data.pos, data.gameBoard[data.pos[0]][data.pos[1]])
                else:  # by size
                    return self.actionObjectBySize(data.gameBoard, data.pos, data.actionOption, data.gameBoard[data.pos[0]][data.pos[1]])

            elif data.actionOption[0] == 4:  # if go rule
                return self.actionObjectByGo(data.gameBoard, data.pos, data.gameBoard[data.pos[0]][data.pos[1]])

            else:
                return SERVER_ERROR

        except Exception as e:
            return SERVER_ERROR

    class GoRule:
        def checkBoard(self, board, pos):
            pi, pj = pos
            me = board[pi][pj]
            you = -me

            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            visit = [[0 for i in range(len(board[0]))] for j in range(len(board))]
            stack = [[pi, pj]]

            while stack:
                i, j = stack.pop()
                visit[i][j] = 1

                for d in dirs:
                    ni, nj = d[0] + i, d[1] + j
                    if board[ni][nj] == you or board[ni][nj] == me and visit[ni][nj]:
                        continue
                    elif board[ni][nj] == me and not visit[ni][nj]:
                        stack.append([ni, nj])
                    else:
                        return False

            return True

        def remove(self, board, pos, value):
            pi, pj = pos
            me = board[pi][pj]
            you = -me

            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            visit = [[0 for i in range(len(board[0]))] for j in range(len(board))]
            stack = [[pi, pj]]

            while stack:
                i, j = stack.pop()
                visit[i][j] = 1
                board[i][j] = value

                for d in dirs:
                    ni, nj = d[0] + i, d[1] + j
                    if board[ni][nj] == you or visit[ni][nj]:
                        continue
                    elif board[ni][nj] == me and not visit[ni][nj]:
                        stack.append([ni, nj])
                    else:
                        return False

            return True

        def findYou(self, board, pos):
            pi, pj = pos
            me = board[pi][pj]
            you = -me
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            lst = list()

            for d in dirs:
                try:
                    ni, nj = d[0] + pi, d[1] + pj
                    if board[ni][nj] == you:
                        lst.append([ni, nj])
                except Exception as e:
                    pass

            return lst