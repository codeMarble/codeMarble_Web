# -*- coding: utf-8 -*-
"""
    codeMarble_Core.userProgram
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    manage user code information.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys
import time
import random


class UserProgram(object):
    def __init__(self, language, savePath, fileName):
        # parameter setting
        self.savePath = savePath
        self.language = language
        self.inputPath = os.path.join(self.savePath, 'input.txt')
        self.filePath = os.path.join(self.savePath, fileName)
        self.executionPath = os.path.join(self.savePath, "%s_%s" %(str(random.randint(100, 999)), str(time.time())[2:5]))


    def compile(self):
        compileMessage = {'C': ['/usr/bin/gcc', '/usr/bin/gcc', '-o'],
                          'C++': ['/usr/bin/g++', '/usr/bin/g++', '-std=c++11', '-o']}

        # python is not compiled
        if 'python' in self.language:
            pass

        else:
            # compile parameter setting
            compileMessage[self.language].append(self.executionPath)
            compileMessage[self.language].append(self.filePath)

            # compile with execution object & return result
            return compileMessage[self.language]


    def play(self):
        playMessage = {'C': [self.executionPath, self.executionPath, '<', self.inputPath],
                       'C++': [self.executionPath, self.executionPath, '<', self.inputPath],
                       'PYTHON2': ['/usr/bin/python', '/usr/bin/python', self.executionPath, '<', self.inputPath],
                       'PYTHON3': ['/usr/bin/python3', '/usr/bin/python3', self.executionPath, '<', self.inputPath]}

         # run program with execution object & return result
        return playMessage[self.language]
