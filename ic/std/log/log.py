#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции журналирования.
"""

import logging
import os
import os.path
import stat
import traceback

__version__ = (0, 0, 2, 2)

# import config

# Шаблон для использования в современных
# командных оболочках и языках
# программирования таков: \x1b[...m.
# Это ESCAPE-последовательность,
# где \x1b обозначает символ ESC
# (десятичный ASCII код 27), а вместо "..."
# подставляются значения из таблицы,
# приведенной ниже, причем они могут
# комбинироваться, тогда нужно их
# перечислить через точку с запятой.

# атрибуты
# 0 	нормальный режим
# 1 	жирный
# 4 	подчеркнутый
# 5 	мигающий
# 7 	инвертированные цвета
# 8 	невидимый

# цвет текста
# 30 	черный
# 31 	красный
# 32 	зеленый
# 33 	желтый
# 34 	синий
# 35 	пурпурный
# 36 	голубой
# 37 	белый

# цвет фона
# 40 	черный
# 41 	красный
# 42 	зеленый
# 43 	желтый
# 44 	синий
# 45 	пурпурный
# 46 	голубой
# 47 	белый

# Цвета в консоли
RED_COLOR_TEXT = '\x1b[31;1m'   # red
GREEN_COLOR_TEXT = '\x1b[32m'   # green
YELLOW_COLOR_TEXT = '\x1b[33m'  # yellow
BLUE_COLOR_TEXT = '\x1b[34m'    # blue
PURPLE_COLOR_TEXT = '\x1b[35m'  # purple
CYAN_COLOR_TEXT = '\x1b[36m'    # cyan
WHITE_COLOR_TEXT = '\x1b[37m'   # white
NORMAL_COLOR_TEXT = '\x1b[0m'   # normal

# Кодировка по умолчанию
DEFAULT_ENCODING = 'utf-8'


def print_color_txt(sTxt, sColor=NORMAL_COLOR_TEXT):
    if type(sTxt) == unicode:
        if CONFIG is not None:
            sTxt = sTxt.encode(CONFIG.DEFAULT_ENCODING)
        else:
            sTxt = sTxt.encode(DEFAULT_ENCODING)
    txt = sColor+sTxt+NORMAL_COLOR_TEXT
    print(txt)        

# Модуль конфигурации
CONFIG = None


def init(mConfig=None, sLogFileName=None):
    """
    Инициализация файла лога.
    @param mConfig: Модуль конфигурации.
    """
    global CONFIG
    CONFIG = mConfig
    
    if not CONFIG.LOG_MODE:
        return
    
    if sLogFileName is None:
        sLogFileName = CONFIG.LOG_FILENAME
        
    # Создать папку логов если она отсутствует
    log_dirname = os.path.normpath(os.path.dirname(sLogFileName))
    if not os.path.exists(log_dirname):
        os.makedirs(log_dirname)
        
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=sLogFileName,
                        filemode='a')
    # ВНИМАНИЕ! сразу выставить права для записи/чтения для всех
    # иначе в ряде случаев может не производится запись в файл и поэтому падать
    if os.path.exists(sLogFileName):
        os.chmod(sLogFileName,
                 stat.S_IWUSR | stat.S_IRUSR |
                 stat.S_IWGRP | stat.S_IRGRP |
                 stat.S_IWOTH | stat.S_IROTH)

    if CONFIG.DEBUG_MODE:
        print_color_txt('INFO. Init log %s' % sLogFileName, GREEN_COLOR_TEXT)


def debug(sMsg=u'', bForcePrint=False, bForceLog=False):
    """
    Вывести ОТЛАДОЧНУЮ информацию.
    @param sMsg: Текстовое сообщение.
    @param bForcePrint: Принудительно вывести на экран.
    @param bForceLog: Принудительно записать в журнале.
    """
    global CONFIG
    
    if CONFIG:
        if CONFIG.DEBUG_MODE or bForcePrint:
            print_color_txt('DEBUG. '+sMsg, BLUE_COLOR_TEXT)
        if CONFIG.LOG_MODE or bForceLog:
            logging.debug(sMsg)
    else:
        print_color_txt('Not init log system.', PURPLE_COLOR_TEXT)
        print_color_txt('DEBUG. ' + sMsg, BLUE_COLOR_TEXT)


def info(sMsg=u'', bForcePrint=False, bForceLog=False):
    """
    Вывести ТЕКСТОВУЮ информацию.
    @param sMsg: Текстовое сообщение.
    @param bForcePrint: Принудительно вывести на экран.
    @param bForceLog: Принудительно записать в журнале.
    """
    global CONFIG
    
    if CONFIG:
        if CONFIG.DEBUG_MODE or bForcePrint:
            print_color_txt('INFO. '+sMsg, GREEN_COLOR_TEXT)
        if CONFIG.LOG_MODE or bForceLog:
            logging.info(sMsg)    
    else:
        print_color_txt('Not init log system.', PURPLE_COLOR_TEXT)
        print_color_txt('INFO. ' + sMsg, GREEN_COLOR_TEXT)


def error(sMsg=u'', bForcePrint=False, bForceLog=False):
    """
    Вывести ОБЩУЮ информацию.
    @param sMsg: Текстовое сообщение.
    @param bForcePrint: Принудительно вывести на экран.
    @param bForceLog: Принудительно записать в журнале.
    """
    global CONFIG
    
    if CONFIG:
        if CONFIG.DEBUG_MODE or bForcePrint:
            print_color_txt('ERROR. '+sMsg, RED_COLOR_TEXT)
        if CONFIG.LOG_MODE or bForceLog:
            logging.error(sMsg)    
    else:
        print_color_txt('Not init log system.', PURPLE_COLOR_TEXT)
        print_color_txt('ERROR. ' + sMsg, RED_COLOR_TEXT)


def warning(sMsg=u'', bForcePrint=False, bForceLog=False):
    """
    Вывести информацию ОБ ПРЕДУПРЕЖДЕНИИ.
    @param sMsg: Текстовое сообщение.
    @param bForcePrint: Принудительно вывести на экран.
    @param bForceLog: Принудительно записать в журнале.
    """
    global CONFIG
    
    if CONFIG:
        if CONFIG.DEBUG_MODE or bForcePrint:
            print_color_txt('WARNING. '+sMsg, YELLOW_COLOR_TEXT)
        if CONFIG.LOG_MODE or bForceLog:
            logging.warning(sMsg)    
    else:
        print_color_txt('Not init log system.', PURPLE_COLOR_TEXT)
        print_color_txt('WARNING. ' + sMsg, YELLOW_COLOR_TEXT)


def fatal(sMsg=u'', bForcePrint=False, bForceLog=False):
    """
    Вывести информацию ОБ ОШИБКЕ.
    @param sMsg: Текстовое сообщение.
    @param bForcePrint: Принудительно вывести на экран.
    @param bForceLog: Принудительно записать в журнале.
    """
    global CONFIG

    trace_txt = traceback.format_exc()

    try:
        msg = sMsg+u'\n'+trace_txt
    except UnicodeDecodeError:
        if not isinstance(sMsg, unicode):
            sMsg = unicode(sMsg, CONFIG.DEFAULT_ENCODING)
        if not isinstance(trace_txt, unicode):
            trace_txt = unicode(trace_txt, CONFIG.DEFAULT_ENCODING)
        msg = sMsg+u'\n'+trace_txt

    if CONFIG:
        if CONFIG.DEBUG_MODE or bForcePrint:
            print_color_txt('FATAL. '+msg, RED_COLOR_TEXT)
        if CONFIG.LOG_MODE or bForceLog:
            logging.fatal(msg)
    else:
        print_color_txt('Not init log system.', PURPLE_COLOR_TEXT)
        print_color_txt('FATAL. ' + msg, RED_COLOR_TEXT)
