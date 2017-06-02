#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами установок.
"""

# --- Подключение пакетов ---
import os.path
import re

from ic.std.log import log
try:
    import ConfigParser
except:
    log.error('Import Error ConfigParser')

from . import ic_file

__version__ = (0, 0, 1, 2)

# --- Константы ---
CFG_FILE_EXT = '.cfg'
INI_FILE_EXT = '.ini'


# --- Функции пользователя ---
def icIniLoadParam(INIFileName_, ParamName_):
    """
    Чтение параметра из файла настроек.
    @param INIFileName_: Полное имя файла настроек.
    @param ParamName_: Имя параметра.
    @return: Возвращает значение параметра или 
        None(если параметра нет или ошибка).
    """
    ini_file = None
    try:
        param = None
        ini_file = open(INIFileName_, 'r')
        row = None      # Текущая считанная из файла строка
        while row != '':
            row = ini_file.readline()
            name_value = re.split(r'=', row)
            if name_value[0] == ParamName_:
                param = name_value[1]
                break
        ini_file.close()
        # Убрать символ перевода каретки
        if param[-1] == '\n':
            param = param[:-1]
        return param
    except:
        if ini_file:
            ini_file.close()
        log.fatal()
        return None


def icIniSaveParam(INIFileName_, ParamName_, ParamValue_):
    """
    Чтение параметра из файла настроек.
    @param INIFileName_: Полное имя файла настроек.
    @param ParamName_: Имя параметра.
    @param ParamValue_: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    old_ini = None
    new_ini = None
    try:
        # Файл-источник переименовать в бак файл
        bak_ini_name = ic_file.icChangeExt(INIFileName_, '.bak')
        
        old_ini = open(bak_ini_name, 'r')   # откуда читать
        new_ini = open(INIFileName_, 'w')   # куда писать
        for row in old_ini.readlines():
            # Разделить запись на имя и значение
            name_value = re.split(r'=', row)
            # Если такой параметр найден в файле,
            # тогда заменить его старое значение
            if name_value[0] == ParamName_:
                write_row = ParamName_+'='+ParamValue_
            else:
                # иначе оставить без изменений
                write_row = row
            if write_row[-1] != '\n':
                write_row += '\n'
            # Записать в выходной файл
            new_ini.write(write_row)
        new_ini.close()
        old_ini.close()
        return True
    except:
        if new_ini:
            new_ini.close()
        if old_ini:
            old_ini.close()
        log.fatal()
        return False


def IniLoadParam(INIFileName_, Section_, ParamName_):
    """
    Чтение параметра из файла настроек.
    @param INIFileName_: Полное имя файла настроек.
    @param Section_: Имя секции.
    @param ParamName_: Имя параметра.
    @return: Возвращает значение параметра или 
        None(если параметра нет или ошибка).
    """
    try:
        param = None
        ini_parser = ConfigParser.ConfigParser()
        # Прочитать файл
        ini_parser.read(INIFileName_)
        if ini_parser.has_section(Section_):
            param = ini_parser.get(Section_, ParamName_)
        return param
    except:
        log.fatal(u'Ошибка чтения из конфигурационного файла %s : %s : %s.' % (INIFileName_, Section_, ParamName_))
        return None


def IniSaveParam(INIFileName_, Section_, ParamName_, ParamValue_):
    """
    Запись параметра в файл настроек.
    @param INIFileName_: Полное имя файла настроек.
    @param Section_: Имя секции.
    @param ParamName_: Имя параметра.
    @param ParamValue_: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    ini_file = None
    try:

        ini_file_name = os.path.split(INIFileName_)
        path = ini_file_name[0]
        file = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Если ини-файла нет, то создать его
        if not os.path.isfile(INIFileName_):
            ini_file = open(INIFileName_, 'w')
            ini_file.write('')
            ini_file.close()
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(INIFileName_, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если нет такой секции, то создать ее
        if not ini_parser.has_section(Section_):
            ini_parser.add_section(Section_)

        ini_parser.set(Section_, ParamName_, ParamValue_)

        # Сохранить и закрыть файл
        ini_file = open(INIFileName_, 'w')
        ini_parser.write(ini_file)
        ini_file.close()
        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка записи в конфигурационный файл %s.' % INIFileName_)
        return False


def IniDelParam(INIFileName_, Section_, ParamName_):
    """
    Удалить параметр из секции конфигурационного файла.
    @param INIFileName_: Полное имя файла настроек.
    @param Section_: Имя секции.
    @param ParamName_: Имя параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    ini_file = None
    try:
        if not os.path.isfile(INIFileName_):
            log.warning(u'Файл конфигурации %s не найден.' % INIFileName_)
            return False
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(INIFileName_, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(Section_):
            return False

        # Удалить
        ini_parser.remove_option(Section_, ParamName_)

        # Сохранить и закрыть файл
        ini_file = open(INIFileName_, 'w')
        ini_parser.write(ini_file)
        ini_file.close()

        return True
    except:
        if ini_file:
            ini_file.close()
        log.warning(u'Ошибка удаления из конфигурационного файла %s.' % INIFileName_)
        return False


def IniParamCount(INIFileName_,Section_):
    """
    Количество параметров в секции.
    @param INIFileName_: Полное имя файла настроек.
    @param Section_: Имя секции.
    @return: Возвращает количеств опараметров в секции или -1 в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.isfile(INIFileName_):
            log.warning(u'Файл конфигурации %s не найден.' % INIFileName_)
            return 0
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(INIFileName_, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(Section_):
            return 0
        # Количество параметров в секции
        return len(ini_parser.options(Section_))
    except:
        if ini_file:
            ini_file.close()
        log.fatal()
        return -1


def IniParamNames(INIFileName_, Section_):
    """
    Имена параметров в секции.
    @param INIFileName_: Полное имя файла настроек.
    @param Section_: Имя секции.
    @return: Возвращает список имен параметров в секции или None в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.isfile(INIFileName_):
            log.warning(u'Файл конфигурации %s не найден.' % INIFileName_)
            return None
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(INIFileName_, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(Section_):
            return []
        # Количество параметров в секции
        return ini_parser.options(Section_)
    except:
        if ini_file:
            ini_file.close()
        log.fatal()
        return None


def Ini2Dict(INIFileName_):
    """
    Представление содержимого INI файла в виде словаря.
    @param INIFileName_: Полное имя файла настроек.
    @return: Заполненный словарь или None в случае ошибки.
    """
    ini_file = None
    try:
        if not ic_file.Exists(INIFileName_):
            log.warning(u'Файл конфигурации %s не найден.' % INIFileName_)
            return None
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(INIFileName_, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()
        
        # Заполнение словаря
        dict = {}
        sections = ini_parser.sections()
        for section in sections:
            params = ini_parser.options(section)
            dict[section] = {}
            for param in params:
                param_str = ini_parser.get(section,param)
                try:
                    # Возможно в виде параметра записан словарь/список/None/число и т.д.
                    param_value = eval(param_str)
                except:
                    # Нет вроде строка
                    param_value = param_str
                dict[section][param] = param_value
        
        return dict
    except:
        if ini_file:
            ini_file.close()
        log.fatal()
        return None
        
    
def Dict2Ini(Dict_, INIFileName_):
    """
    Представление/запись словаря в виде INI файла.
    @param Dict_: Исходный словарь.
    @param INIFileName_: Полное имя файла настроек.
    @return: Возвращает результат сохранения True/False.
    """
    ini_file = None
    try:
        if not Dict_:
            log.warning(u'Не верно определен исходный словарь: %s' % Dict_)
            return False

        ini_file_name = ic_file.Split(INIFileName_)
        path = ini_file_name[0]
        filename = ini_file_name[1]
        if not ic_file.IsDir(path):
            ic_file.MakeDirs(path)

        # Если ини-файла нет, то создать его
        if not ic_file.Exists(INIFileName_):
            ini_file = open(INIFileName_, 'w')
            ini_file.write('')
            ini_file.close()
            
        # Создать объект конфигурации
        ini_parser = ConfigParser.ConfigParser()
        ini_file = open(INIFileName_, 'r')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Прописать словарь в объекте конфигурации
        for section in Dict_.keys():
            # Вдруг в качестве ключей числа или т.п.
            section_str = str(section)
            # Если нет такой секции, то создать ее
            if not ini_parser.has_section(section_str):
                ini_parser.add_section(section_str)

            for param in Dict_[section].keys():
                ini_parser.set(section_str, str(param), str(Dict_[section][param]))

        # Сохранить и закрыть файл
        ini_file = open(INIFileName_, 'w')
        ini_parser.write(ini_file)
        ini_file.close()
        
        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal()
        return False
