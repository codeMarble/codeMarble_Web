# -*- coding: utf-8 -*-
"""
    codeMarble_Core.execution
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    manage runing external program.
    :copyright: (c) 2017 by codeMarble
"""

import os
import ptrace
import resource
from errorCode import *


class Execution(object):
    def __init__(self, limitTime=2000):
        self.limitTime = limitTime


    def executeProgram(self, command):
        parentPid = os.getpid()
        pid = os.fork()

        # pid == 0 : user program process, pid != 0 : matchingProgram process(user program process check)
        if pid is 0:
            self.__runProgram(command, parentPid)

        else:
            # trace user program & returned result,running time
            result, time = self.__traceProgram(pid)

            # if success, check running time
            if time > self.limitTime:
                return TIME_OVER, time, False

            elif result is True:
                try:
                    # get user program's next place position
                    with open(str(parentPid) + '.txt') as fp:
                        pos = fp.readline()

                    return pos, time, True  # return next place position, running tiem, result

                except Execution as e:
                    return SERVER_ERROR, time, False

            # fail
            else:
                return result, time, False  # return fail reason, running time, result


    def __runProgram(self, command, pid):
        os.nice(19) # program priority setting

        # redirect stdout to text file
        redirectionSTDOUT = os.open(str(pid) + '.txt', os.O_RDWR | os.O_CREAT)
        os.dup2(redirectionSTDOUT, 1)

        # cpu using time limit
        soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
        resource.setrlimit(resource.RLIMIT_CPU, ((self.limitTime/1000)+1, hard))

        ptrace.traceme()

        # program run
        os.execv(command[0], tuple(command[1:]))


    def __traceProgram(self, pid):
        while True:
            wpid, status, res = os.wait4(pid, 0)

            # normal termination
            if os.WIFEXITED(status):
                return True, res[0]

            # abnormal termination
            elif os.WIFSIGNALED(status):
                try:
                    ptrace.kill(pid)
                except Exception as e:
                    pass

                return RUNTIME_ERROR, res[0]

            else:
                ptrace.syscall(pid, 0)
