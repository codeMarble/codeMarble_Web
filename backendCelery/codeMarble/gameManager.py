# -*- coding: utf-8 -*-
"""
    codeMarble_Core.gameManager
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    manage game process.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys
from copy import deepcopy

from errorCode import *
from gameData import GameData
from execution import Execution
from userProgram import UserProgram
from scriptTemplate import UserRule


class GameManager(object):
    def __init__(self, challenger, champion, placementRule, placementOption, existRule, existOption, actionRule,
                 actionOption, endingRule, endingOption, objectCount, gameBoard, dataBoard, scriptPath=None, problemIndex='scriptTemplate'):
        if type(challenger) is not UserProgram and type(champion) is not UserProgram:
            raise TypeError

        if scriptPath:
            sys.path.insert(0, scriptPath)
        exec 'from {0} import UserRule'.format(problemIndex)

        # parameter setting
        self.challenger = challenger
        self.champion = champion

        self.data = GameData(objectCount, placementRule, placementOption, existRule, existOption, actionRule,
                             actionOption, endingRule, endingOption, gameBoard, dataBoard)

        self.limitTime = 2000

        self.positionData = ''
        self.boardData = ''

        # make rule and execution object
        self.rules = UserRule()
        self.execution = Execution()

        self.addData('  ')


    def playGame(self):
        try:
            flag = False    # Flase : champ turn, True: challenger turn
            userList = [[self.champion, 0], [self.challenger, 0]]

            self.compileUserCode()
            for _ in range((len(self.data.gameBoard) + 1)**2):
                self.makeInputData()

                message, time, isSuccess = self.execution.executeProgram(userList[flag][0].play(), userList[flag][0].savePath)  # run user program
                self.data.message = message

                if not isSuccess:
                    userList[flag][1] += 1
                    result = message

                else:
                    originalGameBoard = deepcopy(self.data.gameBoard)
                    originalDataBoard = deepcopy(self.data.dataBoard)

                    interResult = self.rules.checkPlacementRule(self.data)

                    if interResult is True:
                        interResult = self.rules.checkActionRule(self.data)

                        if interResult is True:
                            interResult = self.rules.checkEndingRule(self.data)

                            if 0 < interResult < 4:
                                print interResult, flag
                                if interResult is 1:
                                    result = 'win' if flag else 'lose'

                                elif interResult is 2:
                                    result = 'lose' if flag else 'win'

                                elif interResult is 3:
                                    result = 'draw'

                                self.changePlayerNBoard(flag, message)
                                break

                    if interResult == SERVER_ERROR:
                        result = interResult
                        break

                    elif type(interResult) is str:
                        result = interResult
                        userList[flag][1] += 1
                        self.data.gameBoard = deepcopy(originalGameBoard)
                        self.data.dataBoard = deepcopy(originalDataBoard)

                if userList[flag][1] > 2:
                    result = 'lose' if flag else 'win'
                    break

                # change boarad setting (champ <-> challenger)
                self.data.resetData()
                self.changePlayerNBoard(flag, message)
                flag = (not flag)

            else:
                result = 'draw'

            return result, self.positionData, self.boardData

        except Exception as e:
            print e
            return SERVER_ERROR, self.positionData, self.boardData


    def changePlayerNBoard(self, flag, result):
        if flag :   # if challenger
            self.addData(result)

            for i in range(len(self.data.gameBoard)):
                for k in range(len(self.data.gameBoard[0])):
                    self.data.gameBoard[i][k] *= -1


        else:   # if champ
            for i in range(len(self.data.gameBoard)):
                for k in range(len(self.data.gameBoard[0])):
                    self.data.gameBoard[i][k] *= -1

            self.addData(result)


    def addData(self, result):
        self.positionData += str(result).strip() + '\n'

        temp = ''
        for line in self.data.gameBoard:
            for i in line:
                temp += (str(i) + ' ')

            temp += '\n'

        self.boardData += temp


    def compileUserCode(self):
        self.execution.executeProgram(self.challenger.compile(), self.challenger.savePath)
        self.execution.executeProgram(self.champion.compile(), self.champion.savePath)


    def makeInputData(self):
        with open(self.challenger.inputPath, 'w') as fp:
            temp = ''
            for line in self.data.gameBoard:
                for i in line:
                    temp += (str(i) + ' ')

                temp += '\n'
            fp.write(temp)