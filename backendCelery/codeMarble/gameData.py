# -*- coding: utf-8 -*-
"""
    codeMarble_Core.userProgram
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys

class GameData(object):
    def __init__(self, userObjectCount, placementRuleNum, placementRuleOption, existRuleNum, existRuleOption,
                 actionRule, actionRuleOption, endingRuleNum, endingRuleOption, gameBoard, dataBoard):
        self.placementRule = placementRuleNum    # int
        self.placementOption = placementRuleOption    # [] or [[n1,n2],...]
        self.existRule = existRuleNum    # [n1,n2,n3], n=1or2
        self.existOption = existRuleOption    # [n1,n2,n3], 1<=n<=3
        self.actionRule = actionRule    # [int, int]
        self.actionOption = actionRuleOption    # int
        self.endingRule = endingRuleNum    # int
        self.endingOption = endingRuleOption    # [n1, n2]
        self.userObjectCount = userObjectCount    # int

        self.gameBoard = gameBoard    # [[n * k] * k]
        self.dataBoard = dataBoard    # [[n * k] * k]

        self.message = None    # None
        self.objectNum = None    # None
        self.pos = None    # None
        self.postPos = None    # None

        self.checkDataType()


    def resetData(self):
        self.message = None
        self.objectNum = None
        self.pos = None
        self.postPos = None


    def checkDataType(self):
        intList = [self.placementRuleNum, self.placementRuleOption1,self.actionRuleNum, self.actionRuleOption1,
                   self.actionRuleOption2, self.endingRuleNum, self.userObjectCount]
        noneList = [self.message, self.objectNum, self.pos, self.postPos]

        lst1dList = [self.existRuleNum, self.existRuleOption, self.endingRuleOption]
        lst2dList = [self.placementRuleOption2]
        squareList = [self.gameBoard, self.dataBoard]

        if not all(type(var) is int for var in intList) or \
                not all(var is None for var in noneList) or \
                not all(type(var) is list for var in lst1dList) or \
                not all(type(var) is list and var and type(var[0]) is list for var in lst2dList) or \
                not all(type(var) is list and var and type(var[0]) is list and len(var) == len(var[0]) for var in squareList):
            return False

        return True
