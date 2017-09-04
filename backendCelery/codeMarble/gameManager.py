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
    def __init__(self, challenger, champion, placementRule, placementOption, existRule, existOption,
                 actionRule, actionOption, endingRule, endingOption, gameBoard, dataBoard, scriptPath=None, problemIndex='scriptTemplate'):
        if type(challenger) is not UserProgram and type(champion) is not UserProgram:
            raise TypeError

        if scriptPath:
            sys.path.insert(0, scriptPath)
        exec 'from {0} import UserRule'.format(problemIndex)

        # parameter setting
        self.challenger = challenger
        self.champion = champion

        self.data = GameData(placementRule, placementOption, existRule, existOption, actionRule, actionOption,
                             endingRule, endingOption, gameBoard, dataBoard)

        self.limitTime = 2000

        self.positionData = ''
        self.boardData = ''

        # make rule and execution object
        self.rules = UserRule()
        self.execution = Execution()


    def playGame(self):
        flag = False    # Flase : champ turn, True: challenger turn
        userList = [[self.champion, 0], [self.challenger, 0]]

        self.compileUserCode()

        for _ in range(len(self.gameBoard)*len(self.gameBoard)*2):
            message, time, isSuccess = self.execution.executeProgram(userList[flag][0].play())  # run user program
            self.data.message = message

            if not isSuccess:
                userList[flag][1] += 1
                result = message

            else:
                result = self.rules.checkPlacementRule(self.data)

                if type(result) is not str:
                    originalGameBoard = deepcopy(self.data.gameBoard)
                    originalDataBoard = deepcopy(self.data.dataBoard)

                    result = self.rules.checkActionRule(self.data)

                    if type(result) is not str:
                        result = self.rules.checkEndingRule(self.data)

                        if type(result) is int and result:
                            if result is 1:
                                return 'win' if flag else 'lose'

                            elif result is 2:
                                return 'lose' if flag else 'win'

                            else:
                                return 'draw'

                if result == SERVER_ERROR or result == GAME_ERROR:
                    return result

                elif type(result) is str:
                    userList[flag][1] += 1
                    self.data.gameBoard = deepcopy(originalGameBoard)
                    self.data.dataBoard = deepcopy(originalDataBoard)

            if userList[flag][1] > 2:
                return 'lose' if flag else 'win'

            # change boarad setting (champ <-> challenger)
            self.data.resetData()
            self.changePlayerNBoard(flag, result)
            flag = (not flag)

        return 'draw'


    def changePlayerNBoard(self, flag, result):
        if flag :   # if challenger
            for i in range(len(self.gameBoard)):
                for k in range(len(self.gameBoard[0])):
                    self.gameBoard[i][k] = -(self.gameBoard[i][k])

            self.addData(result)

        else:   # if champ
            self.addData(result)

            for i in range(len(self.gameBoard)):
                for k in range(len(self.gameBoard[0])):
                    self.gameBoard[i][k] = -(self.gameBoard[i][k])


    def addData(self, result):
        self.positionData += str(result) + '\n'

        temp = ''
        for line in self.gameBoard:
            for i in line:
                temp += (str(i) + ' ')

            temp += '\n'


    def compileUserCode(self):
        self.execution.executeProgram(self.challenger.compile())
        self.execution.executeProgram(self.champion.compile())


if __name__ == '__main__':
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default=os.getcwd(), help='input file(code&rule) directory')
    parser.add_argument('--script', type=str, default='scriptTemplate', help='input script file name')
    parser.add_argument('--rule', type=str, default='rule', help='input rule file name')
    parser.add_argument('--player1', type=str, default='p1', help='input champion code file name')
    parser.add_argument('--player2', type=str, default='p2', help='input challenger code file name')

    parsed, unparsed = parser.parse_known_args()

    if len(unparsed) > 0:
        print("check your argument. if you want help, use 'codemarble --help'.")

    fileInDir = os.listdir(parsed.path)
    fileName = [parsed.script, parsed.rule, parsed.player1, parsed.player2]

    for i in fileInDir:
        for k in fileName:
            if k in i:
                break
    else:
        print('you inputted wrong data.')
        os.exit(0)

    with open(os.path.join(parsed.path, parsed.script+'.grd')) as fp:
        ruleData = fp.read()

    ruleData = json.load(ruleData)























