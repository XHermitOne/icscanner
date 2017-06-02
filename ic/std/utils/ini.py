#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами установок.
INI файлы - много-секционные файлы настройки
CFG файлы - простые файлы настроек

ВНИМАНИЕ! В INI файл имена параметров записываются в нижнем регистре
а имена секций в верхнем

"""

import os.path
import re

try:
    import ConfigParser
except:
    print(u'ERROR! Import error ConfigParser module')


__version__ = (0, 0, 1, 2)


CFG_FILE_EXT = '.cfg'
INI_FILE_EXT = '.ini'


def loadParamCFG(sCFGFileName, sParamName):
    """
    Чтение параметра из файла настроек.
    @type sCFGFileName: C{string}
    @param sCFGFileName: Полное имя файла настроек.
    @type sParamName: C{string}
    @param sParamName: Имя параметра.
    @return: Возвращает значение параметра или 
        None(если параметра нет или ошибка).
    """
    cfg_file = None
    try:
        param = None
        cfg_file = open(sCFGFileName, 'r')
        row = None  # Текущая считанная из файла строка
        while row != '':
            row = cfg_file.readline()
            name_value = re.split(r'=', row)
            if name_value[0] == sParamName:
                param = name_value[1]
                break
        cfg_file.close()
        # Убрать символ перевода каретки
        if param[-1] == '\n':
            param = param[:-1]
        return param
    except:
        if cfg_file:
            cfg_file.close()
        print((u'ERROR! Error load param %s from CFG file %s' % (sParamName, sCFGFileName)))
        raise


def saveParamCFG(sCFGFileName, sParamName, vParamValue):
    """
    Запись параметра в файл настроек.
    @type sCFGFileName: C{string}
    @param sCFGFileName_: Полное имя файла настроек.
    @type sParamName: C{string}
    @param sParamName: Имя параметра.
    @param vParamValue: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    old_cfg = None
    new_cfg = None
    try:
        # Файл-источник переименовать в бак файл
        from . import ic_file
        bak_cfg_name = ic_file.icChangeExt(sCFGFileName, '.bak')
        
        old_cfg = open(bak_cfg_name, 'r')   # откуда читать
        new_cfg = open(sCFGFileName, 'w')   # куда писать
        for row in old_cfg.readlines():
            # Разделить запись на имя и значение
            name_value = re.split(r'=', row)
            # Если такой параметр найден в файле,
            # тогда заменить его старое значение
            if name_value[0] == sParamName:
                write_row = sParamName+'='+vParamValue
            else:
                # иначе оставить без изменений
                write_row = row
            if write_row[-1] != '\n':
                write_row += '\n'
            # Записать в выходной файл
            new_cfg.write(write_row)
        new_cfg.close()
        old_cfg.close()
        return True
    except:
        if new_cfg:
            new_cfg.close()
        if old_cfg:
            old_cfg.close()
        print((u'ERROR! Save param %s in INI file %s' % (sParamName, sCFGFileName)))
        raise
    return False


def loadParamINI(sINIFileName, sSection, sParamName):
    """
    Чтение параметра из файла настроек.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @type sSection: C{string}
    @param sSection: Имя секции.
    @type sParamName: C{string}
    @param sParamName: Имя параметра.
    @return: Возвращает значение параметра или 
        None(если параметра нет или ошибка).
    """
    try:
        param = None
        ini_parser = ConfigParser.ConfigParser()
        # Прочитать файл
        ini_parser.read(sINIFileName)
        if ini_parser.has_section(sSection):
            param = ini_parser.get(sSection, sParamName)
        return param
    except:
        print((u'ERROR! Load param %s.%s from CFG file %s' % (sSection, sParamName, sINIFileName)))
        raise
    return None


def saveParamINI(sINIFileName, sSection, sParamName, vParamValue):
    """
    Запись параметра в файл настроек.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @type sSection: C{string}
    @param sSection: Имя секции.
    @type sParamName: C{string}
    @param sParamName: Имя параметра.
    @param vParamValue: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    ini_file = None
    try:

        ini_file_name = os.path.split(sINIFileName)
        path = ini_file_name[0]
        file = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Если ини-файла нет, то создать его
        if not os.path.isfile(sINIFileName):
            ini_file = open(sINIFileName, 'w')
            ini_file.write('')
            ini_file.close()
            ini_file = None

        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(sINIFileName, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        ini_file = None

        # Если нет такой секции, то создать ее
        if not ini_parser.has_section(sSection):
            ini_parser.add_section(sSection)

        ini_parser.set(sSection, sParamName, vParamValue)

        # Сохранить и закрыть файл
        ini_file = open(sINIFileName, 'w')
        ini_parser.write(ini_file)
        ini_file.close()
        ini_file = None
        return True
    except:
        if ini_file:
            ini_file.close()
        print((u'ERROR! Save param %s.%s in INI file %s' % (sSection, sParamName, sINIFileName)))
        raise
    return False


def delParamINI(sINIFileName, sSection, sParamName):
    """
    Удалить параметр из секции конфигурационного файла.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @type sSection: C{string}
    @param sSection: Имя секции.
    @type sParamName: C{string}
    @param sParamName: Имя параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    ini_file = None
    try:

        if not os.path.isfile(sINIFileName):
            print((u'WARNING! INI file %s not exists' % sINIFileName))
            return False
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(sINIFileName, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        ini_file = None

        # Если такой секции нет
        if not ini_parser.has_section(sSection):
            print((u'WARNING! Section %s not exists in file %s' % (sSection, sINIFileName)))
            return False

        # Удалить
        ini_parser.remove_option(sSection, sParamName)

        # Сохранить и закрыть файл
        ini_file = open(sINIFileName, 'w')
        ini_parser.write(ini_file)
        ini_file.close()
        ini_file = None

        return True
    except:
        if ini_file:
            ini_file.close()
        print((u'ERROR! Delete param %s.%s from INI file %s' % (sSection, sParamName, sINIFileName)))
        raise
    return False


def getParamCountINI(sINIFileName, sSection):
    """
    Количество параметров в секции.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @type sSection: C{string}
    @param sSection: Имя секции.
    @return: Возвращает количеств опараметров в секции или -1 в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.isfile(sINIFileName):
            print((u'WARNING! INI file %s not exists' % sINIFileName))
            return 0
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(sINIFileName, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        ini_file = None

        # Если такой секции нет
        if not ini_parser.has_section(sSection):
            print((u'WARNING! Section %s not exists in file %s' % (sSection, sINIFileName)))
            return 0
        # Количество параметров в секции
        return len(ini_parser.options(sSection))
    except:
        if ini_file:
            ini_file.close()
        print((u'ERROR! INI file: %s Get param count in section %s' % (sINIFileName, sSection)))
        raise
    return -1


def getParamNamesINI(sINIFileName, sSection):
    """
    Имена параметров в секции.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @type sSection: C{string}
    @param sSection: Имя секции.
    @return: Возвращает список имен параметров в секции или None в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.isfile(sINIFileName):
            print((u'WARNING! INI file %s not exists' % sINIFileName))
            return None
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(sINIFileName, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        ini_file = None

        # Если такой секции нет
        if not ini_parser.has_section(sSection):
            print((u'WARNING! Section %s not exists in file %s' % (sSection, sINIFileName)))
            return []
        # Количество параметров в секции
        return ini_parser.options(sSection)
    except:
        if ini_file:
            ini_file.close()
        print((u'ERROR! INI file: %s Get param names in section %s' % (sINIFileName, sSection)))
        raise
    return None


def INI2Dict(sINIFileName):
    """
    Представление содержимого INI файла в виде словаря.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @return: Заполненный словарь или None в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.exists(sINIFileName):
            print((u'WARNING! INI file %s not exists' % sINIFileName))
            return None
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(sINIFileName, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        ini_file = None

        # Заполнение словаря
        dct = {}
        sections = ini_parser.sections()
        for section in sections:
            params = ini_parser.options(section)
            dct[section] = {}
            for param in params:
                param_str = ini_parser.get(section, param)
                try:
                    # Возможно в виде параметра записан словарь/список/None/число и т.д.
                    param_value = eval(param_str)
                except:
                    # Нет вроде строка
                    param_value = param_str
                dct[section][param] = param_value
        
        return dct
    except:
        if ini_file:
            ini_file.close()
        print((u'ERROR! Conver INI file %s to dictionary' % sINIFileName))
        raise
    return None


def Dict2INI(dDict, sINIFileName):
    """
    Представление/запись словаря в виде INI файла.
    @type dDict: C{dictionary}
    @param dDict: Исходный словарь.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @return: Возвращает результат сохранения True/False.
    """
    ini_file = None
    try:
        if not dDict:
            print((u'WARNING! Not define dictionary %s' % dDict))
            return False

        ini_file_name = os.path.split(sINIFileName)
        path = ini_file_name[0]
        file = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Если ини-файла нет, то создать его
        if not os.path.exists(sINIFileName):
            ini_file = open(sINIFileName, 'w')
            ini_file.write('')
            ini_file.close()
            ini_file = None
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(sINIFileName, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        ini_file = None

        # Прописать словарь в объекте конфигурации
        for section in dDict.keys():
            # Вдруг в качестве ключей числа или т.п.
            section_str = str(section)
            # Если нет такой секции, то создать ее
            if not ini_parser.has_section(section_str):
                ini_parser.add_section(section_str)

            for param in dDict[section].keys():
                ini_parser.set(section_str, str(param), str(dDict[section][param]))

        # Сохранить и закрыть файл
        ini_file = open(sINIFileName, 'w')
        ini_parser.write(ini_file)
        ini_file.close()
        
        return True
    except:
        if ini_file:
            ini_file.close()
        print((u'ERROR! Conver dictionary to INI file %s' % sINIFileName))
        raise
    return False
