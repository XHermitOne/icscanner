#!/usr/bin/env python
#  -*- coding: cp1251 -*-

# -----------------------------------------------------------------------------
# Name:       log_parser.py
# Purpose:    Функции разбора логов.
#
# Author:     <Оконешников А.В.>
#
# Created:     8.02.2006
# RCS-ID:
# Copyright:   (c) 2006 Infocentre
# Licence:     $licence:<your licence>$
# -----------------------------------------------------------------------------

"""
Функции разбора стандартных логов.
"""
import os
import os.path

#   Список ключей лог файла
LogKeyList = ['EXCELNAME','ERROR','REPORT','WARNING']

#   Разделитель блоков лога
LogBlockDiv = '==================================='

def getLineKey(line):
    """
    Возвращает ключ строки.
    """
    line = line.rstrip()
    for key in LogKeyList:
        if line.startswith(key):
            return key

def stdLogToDict(fileName, bDel=False):
    """
    Пример лога:
        ========================================================
        WARRNING: Директория C:\!\Ex не существует. Создаем ее.
        ========================================================
        REPORT: Конвертация завершена.
        ...
        
    Лог преобразуется в питоновский словарь ->
        {'WARNING':'...',
          'REPORT':'...' ...}
        
    @type fileName: C{string}
    @param fileName: Полный до файла логов.
    @type bDel: C{bool}
    @param bDel: Признак удаления файла логов после разбоа.
    """
    d = {}
    if os.path.isfile(fileName):
        f = open(fileName)
        
        #   Разбираем по строчкам
        txt = ''
        lastKey = None
        
        for line in f:
            key = getLineKey(line)
            
            if key:
                lastKey = key
                txt += ':'.join(line.split(':')[1:])
            elif lastKey and not line.startswith(LogBlockDiv):
                txt += line
                
            if lastKey and line.startswith(LogBlockDiv):
                d[lastKey] = txt
                txt = ''
                lastKey = None
    
        if lastKey:
            d[lastKey] = txt
    
        f.close()
        
        if bDel:
            os.remove(fileName)
    else:
        d['ERROR'] = 'Файл логов %s не найден.' % fileName
        
    return d
    
def test():
    #  Тестируем stdLogToDict
    d = stdLogToDict('V:/pythonprj/icservice/dist/econvert.log')
    print(' .... LogDict:', d)
    
if __name__ == "__main__":
    test()