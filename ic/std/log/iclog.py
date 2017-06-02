#!/usr/bin/env python
# -*- coding: windows-1251 -*-

#----------------------------------------------------------------------
# Name:         iclog
# Purpose:      Создание и ведение лога системы
#
# Author:       Okoneshnikov Andei
#
# Created:      29-Aug-2002
# Changed:      iclog.py,v 1.1 2002/11/22 11:37:06
# Copyright:    (c) 2002 by InfoCentre
#----------------------------------------------------------------------
from services.ic_std.utils import ic_mode
if ic_mode.isDebugMode():
    print('import',__file__)

import os
import re
import traceback, sys
try:
    from services.ic_std.dlg.msgbox import MsgBox
except:
    pass

IC_CONSOLE_LOGTYPE = 0
IC_FILE_LOGTYPE = 1
IC_WIN_LOGTYPE = 2
IC_MSGBOX_LOGTYPE = 3

#   Выдает сообщение о последней ошибке
def MsgLastError(parent, beg_msg):
    '''
    Выводит сообщение о последней ошибке в диалоговое окно.

    @type parent: C{wxWindow}
    @param parent: Родительское окно.
    @type beg_msg: C{string}
    @param beg_msg: Заголовок сообщения об ошибке.
    '''

    trace = traceback.extract_tb(sys.exc_traceback)
    last = len(trace) - 1
    ltype = sys.exc_type
    msg = ''

    if last >= 0:
        lt = trace[last]
        msg = beg_msg + ' in file: %s, func: %s, line: %i, \ntext: %s\ntype:%s' % (lt[0], lt[2], lt[1], lt[3],str(ltype))
        MsgBox(parent, msg)

    return msg

def LogLastError(beg_msg, logType = 0):
    '''
    Записывает сообщение о последней ошибке в лог.

    @type beg_msg: C{string}
    @param beg_msg: Заголовок сообщения об ошибке.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1 - файл, 2 - окно лога, 3 - окно сообщений)
    '''

    trace = traceback.extract_tb(sys.exc_traceback)
    ltype = sys.exc_type
    last = len(trace) - 1
    msg = ''

    if last >= 0:
        lt = trace[last]
        msg = beg_msg + ' in file: %s, func: %s, line: %i, \ntext: %s\ntype:%s' % (lt[0], lt[2], lt[1], lt[3],str(ltype))
        toLog(msg, logType)

    return msg

#   Вывод на устройство регистрации специальных сообщений - пока в консоль
def toLog(msg, logType = 0):
    '''
    Вывод на устройство регистрации специальных сообщений.

    @type msg: C{string}
    @param msg: Сообщение об ошибке.
    @type logType: C{int}
    @param logType: Тип лога (0 - консоль, 1 - файл, 2 - окно лога, 3 - окно сообщений)
    '''

    if logType == IC_FILE_LOGTYPE:
        pass
    elif logType  == IC_WIN_LOGTYPE:
        pass
    elif logType == IC_MSGBOX_LOGTYPE:
        MsgBox(None, msg)
    else:
        try:
            print(msg)
        except: pass