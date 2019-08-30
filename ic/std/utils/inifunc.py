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

__version__ = (0, 1, 1, 2)

CFG_FILE_EXT = '.cfg'
INI_FILE_EXT = '.ini'
DEFAULT_ENCODE = 'utf-8'


def loadParamCFG(cfg_filename, param_name):
    """
    Чтение параметра из файла настроек.
    @type cfg_filename: C{string}
    @param cfg_filename: Полное имя файла настроек.
    @type param_name: C{string}
    @param param_name: Имя параметра.
    @return: Возвращает значение параметра или 
        None(если параметра нет или ошибка).
    """
    cfg_file = None
    try:
        param = None
        cfg_file = open(cfg_filename, 'rt')
        row = None  # Текущая считанная из файла строка
        while row != '':
            row = cfg_file.readline()
            name_value = re.split(r'=', row)
            if name_value[0] == param_name:
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
        log.fatal(u'Ошибка загрузки параметра [%s] из CFG файла <%s>' % (param_name, cfg_filename))
    return None


def saveParamCFG(cfg_filename, param_name, param_value):
    """
    Запись параметра в файл настроек.
    @type cfg_filename: C{string}
    @param cfg_filename: Полное имя файла настроек.
    @type param_name: C{string}
    @param param_name: Имя параметра.
    @param param_value: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    old_cfg = None
    new_cfg = None
    try:
        # Файл-источник переименовать в бак файл
        bak_cfg_name = os.path.splitext(cfg_filename)[0] + '.bak'
        shutil.copyfile(cfg_filename, bak_cfg_name)
        
        old_cfg = open(bak_cfg_name, 'rt')   # откуда читать
        new_cfg = open(cfg_filename, 'wt')   # куда писать
        for row in old_cfg.readlines():
            # Разделить запись на имя и значение
            name_value = re.split(r'=', row)
            # Если такой параметр найден в файле,
            # тогда заменить его старое значение
            if name_value[0] == param_name:
                write_row = param_name + '=' + param_value
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
        log.fatal(u'Ошибка сохранения параметра [%s] в INI файл <%s>' % (param_name, cfg_filename))
    return False


def loadParamINI(ini_filename, section, param_name):
    """
    Чтение параметра из файла настроек.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @type section: C{string}
    @param section: Имя секции.
    @type param_name: C{string}
    @param param_name: Имя параметра.
    @return: Возвращает значение параметра или 
        None(если параметра нет или ошибка).
    """
    try:
        param = None
        ini_parser = configparser.ConfigParser()
        # Прочитать файл
        ini_parser.read(ini_filename)
        if ini_parser.has_section(section) and ini_parser.has_option(section, param_name):
            param = ini_parser.get(section, param_name)
        return param
    except:
        log.fatal(u'Ошибка загрузки параметра [%s.%s] из INI файла <%s>' % (section, param_name, ini_filename))
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


def saveParamINI(ini_filename, section, param_name, param_value):
    """
    Запись параметра в файл настроек.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @type section: C{string}
    @param section: Имя секции.
    @type param_name: C{string}
    @param param_name: Имя параметра.
    @param param_value: Значение параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    ini_file = None
    try:
        ini_file_name = os.path.split(ini_filename)
        path = ini_file_name[0]
        file = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Если ини-файла нет, то создать его
        if not os.path.isfile(ini_filename):
            ini_file = open(ini_filename, 'wt')
            ini_file.write('')
            ini_file.close()
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если нет такой секции, то создать ее
        if not ini_parser.has_section(section):
            ini_parser.add_section(section)

        if not isinstance(param_value, str):
            param_value = str(param_value)
        ini_parser.set(section, param_name, param_value)

        # Сохранить и закрыть файл
        ini_file = open(ini_filename, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()
        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка сохранения параметра [%s.%s] в INI файл <%s>' % (section, param_name, ini_filename))
    return False


def delParamINI(ini_filename, section, param_name):
    """
    Удалить параметр из секции конфигурационного файла.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @type section: C{string}
    @param section: Имя секции.
    @type param_name: C{string}
    @param param_name: Имя параметра.
    @return: Возвращает результат выполнения операции True/False.
    """
    ini_file = None
    try:
        if not os.path.isfile(ini_filename):
            log.warning(u'INI файл <%s> не найден' % ini_filename)
            return False
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(section):
            log.warning(u'Секция [%s] не существует в файле <%s>' % (section, ini_filename))
            return False

        # Удалить
        ini_parser.remove_option(section, param_name)

        # Сохранить и закрыть файл
        ini_file = open(ini_filename, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()

        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка удаления параметра [%s.%s] из INI файла <%s>' % (section, param_name, ini_filename))
    return False


def getParamCountINI(ini_filename, section):
    """
    Количество параметров в секции.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @type section: C{string}
    @param section: Имя секции.
    @return: Возвращает количеств опараметров в секции или -1 в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.isfile(ini_filename):
            log.warning(u'INI файл <%s> не найден' % ini_filename)
            return 0
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(section):
            log.warning(u'Секция [%s] не существует в файле <%s>' % (section, ini_filename))
            return 0
        # Количество параметров в секции
        return len(ini_parser.options(section))
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'INI файл <%s>. Ошибка определения количества параметров секции [%s]' % (ini_filename, section))
    return -1


def getParamNamesINI(ini_filename, section):
    """
    Имена параметров в секции.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @type section: C{string}
    @param section: Имя секции.
    @return: Возвращает список имен параметров в секции или None в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.isfile(ini_filename):
            log.warning(u'INI файл <%s> не найден' % ini_filename)
            return None
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Если такой секции нет
        if not ini_parser.has_section(section):
            log.warning(u'Секция [%s] не существует в файле <%s>' % (section, ini_filename))
            return []
        # Количество параметров в секции
        return ini_parser.options(section)
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'INI файл <%s>. Ошибка определения имен параметров секции [%s]' % (ini_filename, section))
    return None


def INI2Dict(ini_filename):
    """
    Представление содержимого INI файла в виде словаря.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @return: Заполненный словарь или None в случае ошибки.
    """
    ini_file = None
    try:
        if not os.path.exists(ini_filename):
            log.warning(u'INI файл <%s> не существует' % ini_filename)
            return None
            
        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
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
        log.fatal(u'Ошибка преобразования INI файла <%s> в словарь' % ini_filename)
    return None


def Dict2INI(data_dict, ini_filename, bRewrite=False):
    """
    Представление/запись словаря в виде INI файла.
    @type data_dict: C{dictionary}
    @param data_dict: Исходный словарь.
    @type ini_filename: C{string}
    @param ini_filename: Полное имя файла настроек.
    @param bRewrite: Переписать полностью существующий INI файл?
    @return: Возвращает результат сохранения True/False.
    """
    ini_file = None
    try:
        if not data_dict:
            log.warning(u'Не определен словарь <%s> для сохранения в INI файле' % data_dict)
            return False

        ini_file_name = os.path.split(ini_filename)
        path = ini_file_name[0]
        file = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # Если ини-файла нет, то создать его
        if not os.path.exists(ini_filename) or bRewrite:
            ini_file = open(ini_filename, 'wt')
            ini_file.write('')
            ini_file.close()

        # Создать объект конфигурации
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # Прописать словарь в объекте конфигурации
        for section in data_dict.keys():
            # Вдруг в качестве ключей числа или т.п.
            section_str = str(section)
            # Если нет такой секции, то создать ее
            if not ini_parser.has_section(section_str):
                ini_parser.add_section(section_str)

            for param in data_dict[section].keys():
                ini_parser.set(section_str, str(param), str(data_dict[section][param]))

        # Сохранить и закрыть файл
        ini_file = open(ini_filename, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()
        
        return True
    except:
        if ini_file:
            ini_file.close()
        log.fatal(u'Ошибка сохранения словаря в INI файле <%s>' % ini_filename)
    return False
