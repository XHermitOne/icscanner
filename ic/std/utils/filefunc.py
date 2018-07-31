#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами.
"""

# Подключение библиотек
import os
import os.path
import platform

from ic.std.log import log

# Имя папки прфиля программы
DEFAULT_PROFILE_DIRNAME = '.icreport'


def _pathFilter(Path_, Filter_):
    """
    Фильтрация путей.
    @return: Возвращает True если папок с указанными имена в фильтре нет в пути и
        False если наоборот.
    """
    path = os.path.normpath(Path_).replace('\\', '/')
    path_lst = path.split('/')
    filter_result = True
    for cur_filter in Filter_:
        if cur_filter in path_lst:
            filter_result = False
            break
    return filter_result


# Папки, которые не надо обрабатывать по умолчанию
DEFAULT_DIR_FILTER = ('.svn', '.SVN', '.Svn', '.idea', '.Idea', '.IDEA')


def getSubDirsFilter(Path_, Filter_=DEFAULT_DIR_FILTER):
    """
    Функция возвращает список поддиректорий с отфильтрованными папками.
    @param Path_: Дeрикторий.
    @param Filter_: Список недопустимых имен папок.
    @return: В случае ошибки возвращает None.
    """
    try:
        dir_list = [os.path.normpath(Path_+'/'+path) for path in os.listdir(Path_)]
        dir_list = [path for path in dir_list if os.path.isdir(path)]
        dir_list = [dir for dir in dir_list if _pathFilter(dir, Filter_)]
        return dir_list
    except:
        log.error('Read subfolder list error <%s>' % Path_)
        return None


def getFilesByExt(Path_, Ext_):
    """
    Функция возвращает список всех файлов в директории с указанным расширением.
    @param Path_: Путь.
    @param Ext_: Расширение, например '.pro'.
    @return: В случае ошибки возвращает None.
    """
    try:
        Path_ = os.path.abspath(os.path.normpath(Path_))

        # Приведение расширения к надлежащему виду
        if Ext_[0] != '.':
            Ext_ = '.'+Ext_
        Ext_ = Ext_.lower()

        file_list = None
        file_list = [os.path.normpath(Path_+'/'+path) for path in os.listdir(Path_)]
        file_list = [path for path in file_list if os.path.isfile(path) and os.path.splitext(path)[1].lower() == Ext_]
        return file_list
    except:
        log.error('Read folder file list error. ext: <%s>, path: <%s>, list: <%s>' % (Ext_, Path_, file_list))
        return None


def getHomePath():
    """
    Путь к домашней директории.
    @return: Строку-путь до папки пользователя.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'windows':
        home_path = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
        home_path = home_path.replace('\\', '/')
    elif os_platform == 'linux':
        home_path = os.environ['HOME']
    else:
        log.warning(u'Not supported OS platform <%s>' % os_platform)
        return None
    return os.path.normpath(home_path)


def getProfilePath(bAutoCreatePath=True):
    """
    Папка профиля программы.
    @param bAutoCreatePath: Создать автоматически путь если его нет?
    @return: Путь до профиля программы.
    """
    home_path = getHomePath()
    if home_path:
        profile_path = os.path.join(home_path, DEFAULT_PROFILE_DIRNAME)
        if not os.path.exists(profile_path) and bAutoCreatePath:
            # Автоматическое создание пути
            try:
                os.makedirs(profile_path)
            except OSError:
                log.fatal(u'Ошибка создания пути профиля <%s>' % profile_path)
        return profile_path
    return '~/' + DEFAULT_PROFILE_DIRNAME
