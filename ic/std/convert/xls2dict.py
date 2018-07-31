#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль конвертора файлов Excel в xls формате в словарь.
"""

# --- Подключение библиотек ---
import os.path
import sys
import win32api
import win32com.client
import pythoncom

from . import xml2dict

__version__ = (0, 0, 1, 2)

# --- Константы ---
# XML формат файла Excel
xlXMLSpreadsheet = 46


# --- Описания функций ---
def XlsFile2Dict(XLSFileName_):
    """
    Функция конвертации файлов Excel в xls формате в формат словаря Python.
    @param XLSFileName_: Имя xls файла. 
    @return: Функция возвращает заполненный словарь, 
        или None в случае ошибки.
    """
    try:
        XLSFileName_ = os.path.abspath(XLSFileName_)
        xml_file_name = os.path.splitext(XLSFileName_)[0]+'.xml'
        # Установить связь с Excel
        excel_app = win32com.client.Dispatch('Excel.Application')
        # Сделать приложение невидимым
        excel_app.Visible = 0
        # Закрыть все книги
        excel_app.Workbooks.Close()
        # Загрузить *.xls файл
        excel_app.Workbooks.Open(XLSFileName_)
        # Сохранить в xml файле
        excel_app.ActiveWorkbook.SaveAs(xml_file_name, FileFormat=xlXMLSpreadsheet)
        # Выйти из Excel
        excel_app.Quit()

        return xml2dict.XmlFile2Dict(xml_file_name)
    except pythoncom.com_error:
        # Вывести сообщение об ошибке в лог
        info = sys.exc_info()[1].args[2][2]
        win32api.MessageBox(0, u'Ошибка чтения файла %s : %s.' % (XLSFileName_, info))
        return None

    except:
        info = sys.exc_info()[1]
        win32api.MessageBox(0, u'Ошибка чтения файла %s : %s.' % (XLSFileName_, info))
        return None

if __name__ == '__main__':
    print((XlsFile2Dict('num_formats.xls')))
