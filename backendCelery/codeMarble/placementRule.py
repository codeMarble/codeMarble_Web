# -*- coding: utf-8 -*-
"""
    codeMarble_Core.placementRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    extract placement position data from output message and apply placement rule.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys

from errorCode import *


class PlacementRule(object):
    def __init__(self):
        pass


    # placementRuleNum(1:add, 2:move), placementRuleOption([]or [[],...])
    # existRuleNum([ally, enemy, extra], 1or2), existRuleOption([ally, enemy, extra], 1or2or3)
    # userObjectCount(n)
    def checkPlacementRule(self, data):
        try:
            interResult = self.applyPlacementRule(data)
            destinationState = data.gameBoard[data.pos[0]][data.pos[1]]

            if abs(destinationState) > 3:
                interResult = self.applyExtraExistRule(data)

            elif destinationState > 0:
                interResult = self.applyAllyExistRule(data)

            else:
                interResult = self.applyEnemyExistRule(data)

            return interResult

        except Exception as e:
            return SERVER_ERROR


    def applyPlacementRule(self,data):
        matrixSize = len(data.gameBoard)

        if not self.splitUserOutput(data):
            return OUTPUT_ERROR

        try:
            row, col = data.pos
            if row < 0 or row >= matrixSize or col < 0 or col >= matrixSize:  # check placement position is in gameBoard
                return OUT_OF_RANGE + '(%d,%d)' % (row, col)

        except Exception as e:
            return OUTPUT_ERROR

        # if placementRule is adding object
        if data.placementRule is 1:
            direct1 = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            direct2 = [[1, 1], [-1, 1], [-1, -1], [1, -1]]


            if data.placementOption[data.objectNum - 1] is 0:
                return True

            elif data.placementOption[data.objectNum - 1] < 3:
                direct = direct1 if data.placementOption is 1 else direct2

            else:
                direct = direct1 + direct2

            for dRow, dCol in direct:  # check option for adding rule.
                tr, tc = row + dRow, col + dCol

                if (tr < matrixSize and tr >= 0) and (tc < matrixSize and tc >= 0):
                    if data.gameBoard[tr][tc] > 0 and data.gameBoard[tr][tc] < 4:  # if it fits option rule, break for statement
                        break
            else:
                return MISS_POSITION + '(%d,%d)'%(row, col)

        # if placementRule is moving object
        elif data.placementRule is 2:
            try:
                pastRow, pastCol = data.pastPos

                rowMovingSize = abs(pastRow - row)
                colMovingSize = abs(pastCol - col)  # calculate object moving size

                if (not rowMovingSize) and (not colMovingSize):
                    return MISS_POSITION + '(%d,%d)'%(row, col)

            except Exception as e:
                return OUTPUT_ERROR

            # check the object to move
            if data.objectNum < 0 or data.objectNum > 3:
                return MISS_POSITION + '(%d,%d)'%(row, col)

            # check the rule to move object
            if data.placementOption[data.objectNum - 1][0] is 0:
                pass

            # check move size each object's direction
            elif data.placementOption[data.objectNum - 1][0] < 4:    # ＋ dir
                if not self.checkMovingDirction(data, rowMovingSize, colMovingSize):
                    return MISS_POSITION + '(%d,%d)'%(row, col)

                else:
                    return GAME_ERROR

            else:  # check each object's move path and size
                if rowMovingSize != data.placementOption[data.objectNum - 1][1] or \
                    colMovingSize != data.placementOption[data.objectNum - 1][2]:
                    return MISS_POSITION + '(%d,%d)'%(row, col)

        else:
            return SERVER_ERROR

        return True


    def applyAllyExistRule(self, data):
        if data.existRule[0] is 1:
            return MISS_POSITION + '(%d,%d)'%(data.pos[0], data.pos[1])

        elif data.existRule[0] is 2:
            if data.existOption[0] is 1:
                data.gameBoard[data.pos[0]][data.pos[1]] = data.objectNum

            else:
                pass

        else:
            return SERVER_ERROR

        return True


    def applyEnemyExistRule(self, data):
        if data.existRule[1] is 1:
            return MISS_POSITION + '(%d,%d)'%(data.pos[0], data.pos[1])

        elif data.existRule[1] is 2: #remove
            if data.existOption[1] is 1:  # delete enemy and not move object
                data.gameBoard[data.pos[0]][data.pos[1]] = 0

            elif data.existOption[1] is 2:   # delete enemy and move object
                data.gameBoard[data.pos[0]][data.pos[1]] = data.objectNum
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

            else:   # delete all object
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

        else:
            return GAME_ERROR

        return True


    def applyExtraExistRule(self, data):
        if data.existRule[2] is 1:
            return MISS_POSITION + '(%d,%d)'%(data.pos[0], data.pos[1])

        elif data.existRule[2] is 2:  # remove
            if data.existOption[2] is 1:  # delete enemy and not move object
                data.gameBoard[data.pos[0]][data.pos[1]] = 0

            elif data.existOption[2] is 2:  # delete enemy and move object
                data.gameBoard[data.pos[0]][data.pos[1]] = data.objectNum
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

            else:  # delete all object
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

        else:
            return GAME_ERROR

        return True


    def splitUserOutput(self, data):
        try:
            if data.placementRule is 1:
                if data.userObjectCount is 1:
                    data.pos = [int(i) for i in data.message.split()]
                    data.objectNum = 1

                else:
                    tempData = [int(i) for i in data.message.split()]
                    data.objectNum = tempData[0]
                    data.pos = tempData[1:]

            elif data.placementRule is 2:
                posData = data.message.split('>')

                data.pastPos = [int(i) for i in posData[0].split()]
                data.pos = [int(i) for i in posData[1].split()]
                data.objectNum = data.gameBoard[data.pastPost[0]][data.pastPost[1]]

            else:
                return False

        except Exception as e:
            return False


    def checkMovingDirction(self, data, rowMovingSize, colMovingSize): # check direction and size
        totalSize = rowMovingSize + colMovingSize

        if rowMovingSize == colMovingSize and data.placementOption[data.objectNum - 1][2] == rowMovingSize: # check × dir
            if data.placementOption[data.objectNum - 1][0] is 1:
                return False

        elif (totalSize == rowMovingSize or totalSize == colMovingSize) and data.placementOption[data.objectNum - 1][2] == totalSize: # check ＋ dir
            if data.placementOption[data.objectNum - 1][0] is 2:
                return False

        else:
            return False

        if data.placementOption[data.objectNum - 1][1]: # check other object in direction way
            posList = zip(range(data.postPos[0], data.pos[0]), range(data.postPos[1], data.pos[1]))

            for tRow, tCol in posList[1:]:
                if 0 < abs(data.gameBoard[tRow][tCol]) < 4:
                    return False

        return True