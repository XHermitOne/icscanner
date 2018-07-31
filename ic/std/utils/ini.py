#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами установок.
INI файлы - много-секционные файлы настройки
CFG файлы - простые файлы настроек

ВНИМАНИЕ! В INI файл имена параметров записываются в нижнем регистре
а имена секций в верхнем
"""

import os
import os.path
import shutil
import re

from ..log import log

try:
    import configparser
except ImportError:
    log.error('Ошибка импорта configparser', bForcePrint=True)

__version__ = (0, 1, 1, 1)

CFG_FILE_EXT = '.cfg'
INI_FILE_EXT = '.ini'
DEFAULT_ENCODE = 'utf-8'


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
        cfg_file = open(sCFGFileName, 'rt')
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
        log.fatal(u'Ошибка загрузки параметра [%s] из CFG файла <%s>' % (sParamName, sCFGFileName))
    return None


def saveParamCFG(sCFGFileName, sParamName, vParamValue):
    """
    Запись параметра в файл настроек.
    @type sCFGFileName: C{string}
    @param sCFGFileName: Полное имя файла настроек.
    @type sParamName: C{string}
    @param sParamName: Имя параметра.
    @param vParamValue: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    old_cfg = None
    new_cfg = None
    try:
        # Файл-источник переименовать в бак файл
        bak_cfg_name = os.path.splitext(sCFGFileName)[0] + '.bak'
        shutil.copyfile(sCFGFileName, bak_cfg_name)
        
        old_cfg = open(bak_cfg_name, 'rt')   # откуда читать
        new_cfg = open(sCFGFileName, 'wt')   # куда писать
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
        log.fatal(u'Ошибка сохранения параметра [%s] в INI файл <%s>' % (sParamName, sCFGFileName))
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
        ini_parser = configparser.ConfigParser()
        # Прочитать файл
        ini_parser.read(sINIFileName)
        if ini_parser.has_section(sSection) and ini_parser.has_option(sSection, sParamName):
            param = ini_parser.get(sSection, sParamName)
        return param
    except:
        log.fatal(u'Ошибка загрузки параметра [%s.%s] из INI файла <%s>' % (sSection, sParamName, sINIFileName))
    return None


def loadParamINIValue(*args, **kwargs):
    """
    Чтение параметра из файла настроек.
    @return: Происходит попытка прееобразование из строки возвращаемого
        значения к реальному типу по средством <eval>.
        Если при преобразовании возникла ошибка, то возвращается строка.
    """
    param = loadParamINI(*args, **kwargs)
    try:
        value = eval(param)
    except:
        value = param
    return value


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
            ini_file = open(sINIFileName, 'wt')
            ini_file.write('')
            ini_file.close()
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(sINIFileName, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если нет такой секции, то создать ее
        if not ini_parser.has_section(sSection):
            ini_parser.add_section(sSection)

        if not isinstance(vParamValue, str):
            vParamValue = str(vParamValue)
        ini_parser.set(sSection, sParamName, vParamValue)

        # Сохранить и закрыть файл
        ini_file = open(sINIFileName, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()
        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка сохранения параметра [%s.%s] в INI файл <%s>' % (sSection, sParamName, sINIFileName))
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
            log.warning(u'INI файл <%s> не найден' % sINIFileName)
            return False
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(sINIFileName, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(sSection):
            log.warning(u'Секция [%s] не существует в файле <%s>' % (sSection, sINIFileName))
            return False

        # Удалить
        ini_parser.remove_option(sSection, sParamName)

        # Сохранить и закрыть файл
        ini_file = open(sINIFileName, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()

        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка удаления параметра [%s.%s] из INI файла <%s>' % (sSection, sParamName, sINIFileName))
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
            log.warning(u'INI файл <%s> не найден' % sINIFileName)
            return 0
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(sINIFileName, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(sSection):
            log.warning(u'Секция [%s] не существует в файле <%s>' % (sSection, sINIFileName))
            return 0
        # Количество параметров в секции
        return len(ini_parser.options(sSection))
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'INI файл <%s>. Ошибка определения количества параметров секции [%s]' % (sINIFileName, sSection))
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
            log.warning(u'INI файл <%s> не найден' % sINIFileName)
            return None
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(sINIFileName, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(sSection):
            log.warning(u'Секция [%s] не существует в файле <%s>' % (sSection, sINIFileName))
            return []
        # Количество параметров в секции
        return ini_parser.options(sSection)
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'INI файл <%s>. Ошибка определения имен параметров секции [%s]' % (sINIFileName, sSection))
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
            log.warning(u'INI файл <%s> не существует' % sINIFileName)
            return None
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(sINIFileName, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()
        
        # Заполнение словаря
        dict = {}
        sections = ini_parser.sections()
        for section in sections:
            params = ini_parser.options(section)
            dict[section] = {}
            for param in params:
                param_str = ini_parser.get(section, param)
                try:
                    # Возможно в виде параметра записан
                    # словарь/список/None/число и т.д.
                    param_value = eval(param_str)
                except:
                    # Нет вроде строка
                    param_value = param_str
                dict[section][param] = param_value
        
        return dict
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка преобразования INI файла <%s> в словарь' % sINIFileName)
    return None


def Dict2INI(dDict, sINIFileName, rewrite=False):
    """
    Представление/запись словаря в виде INI файла.
    @type dDict: C{dictionary}
    @param dDict: Исходный словарь.
    @type sINIFileName: C{string}
    @param sINIFileName: Полное имя файла настроек.
    @param rewrite: Переписать полностью существующий INI файл?
    @return: Возвращает результат сохранения True/False.
    """
    ini_file = None
    try:
        if not dDict:
            log.warning(u'Не определен словарь <%s> для сохранения в INI файле' % dDict)
            return False

        ini_file_name = os.path.split(sINIFileName)
        path = ini_file_name[0]
        file = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Если ини-файла нет, то создать его
        if not os.path.exists(sINIFileName) or rewrite:
            ini_file = open(sINIFileName, 'wt')
            ini_file.write('')
            ini_file.close()

        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(sINIFileName, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

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
        ini_file = open(sINIFileName, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()
        
        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка сохранения словаря в INI файле <%s>' % sINIFileName)
    return False
