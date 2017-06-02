#!/usr/bin/env python
# -*- coding: cp1251 -*-

# ----------------------------------------------------------------------
# Name:         ic.ic_run.ic_log
# Purpose:      Создание и ведение лога системы
#
# Author:       Шурик Колчанов
#
# Created:      29-Aug-2002
# Changed:      v. 1.0 2002/08/29 14:37:06
# Copyright:    (c) 2002 by InfoCentre
# ----------------------------------------------------------------------
from services.ic_std.utils import ic_mode
if ic_mode.isDebugMode():
    print('import',__file__)

import sys
import services.ic_std.log.iclog
import services.ic_std.utils.ic_codecs as ic_codecs

#Выдает сообщение о последней ошибке на экран
def icMsgErr(parent, msg):
    '''
    Выдает сообщение о последней ошибке на экран.
    '''
    return services.ic_std.log.iclog.MsgLastError(parent, msg)

#Выдает сообщение о последней ошибке в регистратор
def icLogErr(msg=''):
    '''
    Выдает сообщение о последней ошибке в регистратор.
        Эту функцию можно использовать только в блоке exception.
    '''
    string=''
    if msg<>'':
        string=ic_codecs.ReCodeString(msg,'CP1251','CP866')
    return services.ic_std.log.iclog.LogLastError(string)

#Выдает сообщение в регистратор (на консоль)
#import ic.icEditor.CfgSysProc
def icToLog(msg):
    '''
    Выдает сообщение в регистратор (на консоль).
    @param msg: Текст сообщения.
    '''
    string=ic_codecs.ReCodeString(msg,'CP1251','CP866')
    return services.ic_std.log.iclog.toLog(string)

def icWin32Err():
    '''
    Вывод ошибок Microsoft.
    '''
    #Получено экспериментальным путем
    info=sys.exc_info()[1].args
    err_txt=str(info)
    f=open('win32.err', 'w')
    f.write(info[2])
    f.write(err_txt)
    f.close()
    return icToLog(err_txt)

def icODBCErr():
    '''
    Вывод ошибок Microsoft ODBC.
    '''
    #Получено экспериментальным путем
    err_txt=sys.exc_info()[1].args[2]
    return icToLog(err_txt)
