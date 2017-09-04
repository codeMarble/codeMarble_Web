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
        self.language = language
        self.filePath = os.path.join(savePath, fileName)
        self.executionPath = os.path.join(savePath, "%s_%s" %(str(random.randint(1, 100)) + str(time.time())[2:5]))


    def compile(self):
        compileMessage = {'C': ['/usr/bin/gcc', '/usr/bin/gcc', '-o'],
                          'C++': ['/usr/bin/g++', '/usr/bin/g++', '-std=c++11', '-o']}

        # python is not compiled
        if 'python' in self.language:
            pass

        else:
            # compile parameter setting
            compileMessage[self.language].append(self.filePath)
            compileMessage[self.language].append(self.executionPath)

            # compile with execution object & return result
            return compileMessage[self.language]


    def play(self):
        playMessage = {'C': [self.executionPath, self.executionPath, '<'],
                       'C++': [self.executionPath, self.executionPath, '<'],
                       'PYTHON2': ['/usr/bin/python', '/usr/bin/python', self.executionPath, '<'],
                       'PYTHON3': ['/usr/bin/python3', '/usr/bin/python3', self.executionPath, '<']}

         # run program with execution object & return result
        return playMessage[self.language]
