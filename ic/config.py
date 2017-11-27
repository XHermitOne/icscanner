#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конфигурационный файл.

Параметры:

@type DEBUG_MODE: C{bool}
@var DEBUG_MODE: Режим отладки (вкл./выкл.)
@type LOG_MODE: C{bool}
@var LOG_MODE: Режим журналирования (вкл./выкл.)
"""

import os
import os.path
import datetime

DEFAULT_ENCODING = 'utf-8'

DEBUG_MODE = True
LOG_MODE = True

# Имя папки прфиля программы
PROFILE_DIRNAME = '.icscanner'
PROFILE_PATH = os.path.join(os.environ.get('HOME', '/home/user'),
                            PROFILE_DIRNAME)

# Имя файла журнала
LOG_FILENAME = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)+'/log'),
                            PROFILE_DIRNAME,
                            'icscanner_%s.log' % datetime.date.today().isoformat())

DEFAULT_OPTIONS_FILENAME = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)),
                                        PROFILE_DIRNAME, 'options.ini')

DEFAULT_SCAN_FILENAME = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)),
                                     PROFILE_DIRNAME, 'scan_output.pdf')

DEFAULT_EXT_SCAN_PRG = 'gscan2pdf&'

# Максимальное количество листов, помещаемых в лоток сканера по умолчанию
DEFAULT_SCANNER_MAX_SHEETS = 60


def get_glob_var(name):
    """
    Прочитать значение глобальной переменной.
    @type name: C{string}
    @param name: Имя переменной.
    """
    return globals()[name]


def set_glob_var(name, value):
    """
    Установить значение глобальной переменной.
    @type name: C{string}
    @param name: Имя переменной.
    @param value: Значение переменной.
    """
    globals()[name] = value
    return value
