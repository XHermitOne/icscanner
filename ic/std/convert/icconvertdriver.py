#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('import',__file__)

"""
Классы драйверов конвертера данных.
"""

#--- Подключение библиотек ---
from ic.utils import ic_file

from ic.components import icwidget
from ic.interfaces import icconvertdriverinterface

#--- Спецификации ---
SPC_IC_CONVERTDRIVER={
    'name':'default',
    'type':'ConvertDriver',
    'source':None, #Источник данных
    '__parent__':icwidget.SPC_IC_SIMPLE,
    }
    
SPC_IC_DBFCONVERTDRIVER={
    'name':'default',
    'type':'DBFConvertDriver',
    'dbf_file':None, #Имя DBF файла источника данных
    'dbf_field': None, #Имя поля DBF файла источника данных
    '__parent__':SPC_IC_CONVERTDRIVER,
    }
    
#--- Классы ---
class icConvertDriverPrototype(icconvertdriverinterface.icConvertDriverInterface):
    """
    Базовый класс драйверов конвертера данных.
    """
    def __init__(self,component_spc=None):
        """
        Конструктор.
        """
        icconvertdriverinterface.icConvertDriverInterface.__init__(self,component_spc)

from ic.db import dbf

class icDBFConvertDriverPrototype(icConvertDriverPrototype):
    """
    Базовый класс драйверов конвертера данных из DBF файлов.
    """
    def __init__(self,component_spc=None):
        """
        Конструктор.
        """
        icConvertDriverPrototype.__init__(self,component_spc)
        
        self._data_src=None

    def _open(self):
        """
        Открытие источника данных.
        """
        if self._data_src is None:
            dbf_file_name=self.getDBFFileName()
            #print '@@@',dbf_file_name
            self._data_src=dbf.icDBFFile(dbf_file_name)
            self._data_src.Open()
        
    def _close(self):
        """
        Закрытие источника данныъх.
        """
        if self._data_src:
            self._data_src.Close()
            self._data_src=None
            
    def getDBFFileName(self):
        """
        Имя DBF файла - источника данных.
        """
        dbf_file_name=self.resource['dbf_file']
        if dbf_file_name: 
            return ic_file.AbsolutePath(dbf_file_name)
        return None
        
    def First(self):
        """
        Переход на первый индекс.
        """
        self._open()
        return self._data_src.First()
        
    def Last(self):
        """
        Переход на последний индекс.
        """
        self._open()
        return self._data_src.Last()
        
    def Next(self):
        """
        Переход  к следующему элементу.
        """
        self._open()
        return self._data_src.Next()
        
    def Prev(self):
        """
        Переход к предыдущему элементу.
        """
        self._open()
        return self._data_src.Prev()
        
    def IsEnd(self):
        """
        Проверка достижения конца последовательности данных.
        """
        self._open()
        return self._data_src.EOF()
        
    def IsBegin(self):
        """
        Проверка достижения начала последорвательности данных.
        """
        self._open()
        return self._data_src.BOF()
        
    def getDataByName(self,Name_):
        """
        Получить данные по имени.
        """
        self._open()
        #print '@@@',Name_
        return self._data_src.getFieldByName(Name_)

