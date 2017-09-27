# -*- coding: utf-8 -*-

import os
import sys
import shutil
import zipfile

from flask import request, redirect, session, url_for, render_template, flash

from codeMarble_Web.celeryFile import addProblem
from codeMarble_Web.database import dao

from codeMarble_Web.codeMarble_blueprint import *

from codeMarble_Web.utils.utilUserQuery import *
from codeMarble_Web.utils.utilBoardQuery import *
from codeMarble_Web.utils.utilProblemQuery import select_problem, insert_problem
from codeMarble_Web.utils.checkInvalidAccess import check_invalid_access
from codeMarble_Web.utils.loginRequired import login_required


@codeMarble.teardown_request
def close_db_session(exception = None):
    try:
        dao.remove()

    except Exception as e:
        from codeMarble_Web.codeMarble_logger import *
        Log.error(str(e))


@codeMarble.route('/admin', methods=['GET', 'POST'])
@check_invalid_access
def admin():
    return redirect(url_for('.manageProblem'))


@codeMarble.route('/admin/problem', methods=['GET', 'POST'])
@check_invalid_access
def manageProblem():
    try:
        problemList = select_problem()
        return render_template('manageProblem.html',
                               problemList=problemList)

    except Exception as e:
        print e


@codeMarble.route('/admin/subAdmin', methods=['GET', 'POST'])
@check_invalid_access
def manageAdmin():
    try:
        userList = select_user(authority='semiAdmin')
        return render_template('manageAdmin.html',
                               userList=userList)

    except Exception as e:
        print e


@codeMarble.route('/admin/enterSubAdmin', methods=['POST'])
@login_required
@check_invalid_access
def enterSubAdmin():
    if request.method == 'POST':
        try:
            userIndex = select_user(userId=request.form['userId']).first().userIndex
            update_user(userIndex=userIndex, authority='semiAdmin')

            dao.commit()

            return redirect(url_for('.manageAdmin'))

        except AttributeError as e:
            print e
            dao.rollback()

            flash('존재하지 않는 사용자입니다.')
            return redirect(url_for('.manageAdmin'))

        except Exception as e:
            print e
            dao.rollback()

            flash('다시 시도해주세요.')
            return redirect(url_for('.main'))


@codeMarble.route('/admin/deleteSubAdmin<int:userIndex>', methods=['POST'])
@login_required
@check_invalid_access
def deleteSubAdmin(userIndex):
    if request.method == 'POST':
        try:
            update_user(userIndex, authority='user')

            dao.commit()

        except Exception as e:
            print e
            dao.rollback()

            flash('다시 시도해주세요.')
            return redirect(url_for('.main'))


        return redirect(url_for('.main'))


@codeMarble.route('/admin/registerProblem', methods=['POST'])
@login_required
@check_invalid_access
def registerProblem():
    import json

    thisPath, _ = os.path.split(os.path.abspath(__file__))
    _thisPath, _ = os.path.split(thisPath)
    thisPath, _ = os.path.split(_thisPath)
    savePath = os.path.join(thisPath, 'problemData')

    f = request.files.getlist('zipFile')[0]
    f.save(os.path.join(savePath, f.filename))

    fileName = f.filename.split('.')[0]
    tempDir = os.path.join(savePath, fileName)
    tempZip = zipfile.ZipFile(os.path.join(savePath, f.filename))
    tempZip.extractall(tempDir)
    tempZip.close()

    fileList = os.listdir(tempDir)

    if (fileName + '.json' in fileList) and (fileName + '.pdf' in fileList):
        try:
            with open(os.path.join(tempDir, fileName+'.json')) as fp:
                data = json.load(fp)
                tempGameBoard = ''
                tempDataBoard = ''
                tempPlacementOption = ''

                for i in range(len(data['placementOption'])):
                    tempPlacementOption = tempPlacementOption + (' '.join(str(j) for j in data['placementOption'][i])) + '\n'

                for i in range(len(data['gameBoard'])):
                    tempGameBoard += ' '.join(str(j) for j in data['gameBoard'][i]) + '\n'
                    tempDataBoard += ' '.join(str(j) for j in data['dataBoard'][i]) + '\n'

                dao.add(insert_problem(problemName=fileName, placementRule=str(data['placementRule']),
                                       boardSize=data['boardSize'],
                                       placementPoint=data['placementPoint'],
                                       placementOption=tempPlacementOption,
                                       existRule=' '.join(str(i) for i in data['existRule']),
                                       existOption=' '.join(str(i) for i in data['existOption']),
                                       actionRule=str(data['actionRule']),
                                       actionOption=' '.join(str(i) for i in data['actionOption']),
                                       endingRule=str(data['endingRule']), endingOption=' '.join(str(i) for i in data['endingOption']),
                                       gameBoard=tempGameBoard, dataBoard=tempDataBoard))

                shutil.move(tempDir, os.path.join(_thisPath, 'static', 'problems'))

                dao.commit()

            problemIndex = select_problem(problemName=fileName).first().problemIndex

            addProblem.delay(problemIndex, json.dumps(data))

            message = '문제가 등록 됐습니다.'

        except Exception as e:
            print e

            message = '다시 시도하세요.'



    else:
        message = '파일을 다시 확인해 주세요.'


    os.remove(os.path.join(savePath, f.filename))

    flash(message)
    return redirect(url_for('.admin'))

















