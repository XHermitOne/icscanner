#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций выполнения запросов и методов пользователя.
"""

import os
import sys
import imp
from ic.std.log import log

__versiom__ = (0, 0, 0, 2)


def loadSource(name, path):
    """
    Возвращает загруженный модуль.

    @type name: C{string}
    @param name: Имя модуля.
    @type path: C{string}
    @param path: Полный путь до модуля.
    """
    f = open(path)
    mod = imp.load_source(name, path, f)
    f.close()
    return mod


def unLoadSource(name):
    """
    Выгрузить модуль.
    @type name: C{string}
    @param name: Имя модуля.
    """
    if name in sys.modules:
        del sys.modules[name]
        return True
    return False


def reLoadSource(name, path=None):
    """
    Перезагрузить модуль.
    @type name: C{string}
    @param name: Имя модуля.
    @type path: C{string}
    @param path: Полный путь до модуля.
    """
    if path is None:
        if name in sys.modules:
            py_file_name = sys.modules[name].__file__
            py_file_name = os.path.splitext(py_file_name)[0]+'.py'
            path = py_file_name
        else:
            log.warning('Module <%s> not loaded' % name)
            return None
    unLoadSource(name)
    return loadSource(name, path)


def exec_code(sCode='', bReImport=False, name_space=None, kwargs=None):
    """
    Выполнить блок кода.
    @type sCode: C{string}
    @param sCode: Блок кода.
        Блок кода - строка в формате:
            ИмяПакета.ИмяМодуля.ИмяФункции(аргументы).
    @type bReImport: C{bool}
    @param bReImport: Переимпортировать модуль функции?
    @type name_space: C{dictionary}
    @param name_space: Пространство имен.
    @type kwargs: C{dictionary}
    @param kwargs: Дополнительные аргументы функции.
    """
    result = None

    # Подготовить пространство имен
    if name_space is None or not isinstance(name_space, dict):
        name_space = {}

    func_import = sCode.split('(')[0].split('.')
    func_mod = '.'.join(func_import[:-1])

    if bReImport:
        unLoadSource(func_mod)

    # Импортирование модуля
    if func_mod:
        import_str = 'import ' + func_mod
        try:
            exec import_str
        except:
            log.error(u'Import module error <%s>' % import_str)
            raise

    # Добавить локальное пространство имен
    name_space.update(locals())

    if kwargs:
        if isinstance(kwargs, dict):
            name_space.update(kwargs)
        else:
            log.warning(u'Не поддерживаемый тип <%s> дополнительных аргументов функции <%s>' % (type(kwargs), sCode))

    # Выполнение функции
    try:
        result = eval(sCode, globals(), name_space)
    except:
        log.error(u'Execute function error <%s>' % sCode)
        raise

    return result

