#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Создание и ведение лога системы.
@author: Шурик Колчанов.
'''

#--- Подключение библиотек ---
import sys
import traceback

try:
  import win32api
except:
  pass


#--- Функции ---
def msgErr(msg=''):
    '''
    Выдает сообщение о последней ошибке в MessageBox.
        Эту функцию можно использовать только в блоке exception.
    @param msg: Текст сообщения.
    '''
    info=sys.exc_info()
    err_type,err_value,exc_traceback=info[:3]
    err_code=exc_traceback.tb_frame.f_code
    err_lineno=exc_traceback.tb_lineno
    msg+='\nError info:\ntype: %s\nmessage: %s\nmodule: %s\nfunction: %s\nline no: %d'%(err_type,err_value,
         str(err_code.co_filename),str(err_code.co_name),
         err_lineno)
    toMsg(msg)

    return msg

def toMsg(msg):
    '''
    Выдает сообщение в MessageBox.
    @param msg: Текст сообщения.
    '''
    try:
      return win32api.MessageBox(0,msg)
    except:
      print(msg)
