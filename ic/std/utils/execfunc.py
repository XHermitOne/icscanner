#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций выполнения запросов и методов пользователя.
"""

import os
import sys
import imp

from ..log import log

__versiom__ = (0, 1, 1, 2)


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


def exec_code(code_block='', bReImport=False, name_space=None, kwargs=None):
    """
    Выполнить блок кода.
    @type code_block: C{string}
    @param code_block: Блок кода.
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

    func_import = code_block.split('(')[0].split('.')
    func_mod = '.'.join(func_import[:-1])

    if bReImport:
        unLoadSource(func_mod)

    # Импортирование модуля
    if func_mod:
        import_str = 'import ' + func_mod
        try:
            exec(import_str)
        except:
            log.error(u'Import module error <%s>' % import_str)
            raise

    # Добавить локальное пространство имен
    name_space.update(locals())

    if kwargs:
        if isinstance(kwargs, dict):
            name_space.update(kwargs)
        else:
            log.warning(u'Не поддерживаемый тип <%s> дополнительных аргументов функции <%s>' % (type(kwargs), code_block))

    # Выполнение функции
    try:
        result = eval(code_block, globals(), name_space)
    except:
        log.error(u'Execute function error <%s>' % code_block)
        raise

    return result


# Словарь ассоциаций вызова внешних просмотрщиков по расширению файла
ASSOCIATION_VIEW_FILE = {
    ('.pdf',): 'evince %s&',
    ('.jpg', '.jpeg', '.bmp', '.tiff', '.png'): 'eog %s&',
}


def view_file_ext(filename):
    """
    Запуск просмотра файла внешней программой.
    Определение какой программой производить просмотр определяется по расширению файла.
    @param filename: Полное имя файла.
    @return: True/False.
    """
    if not os.path.exists(filename):
        log.warning(u'Просмотр файла внешней программой. Файл <%s> не наден.' % filename)
        return False
    file_type = os.path.splitext(filename)[1]
    file_ext = file_type.lower()

    for file_extensions, view_cmd_associate in ASSOCIATION_VIEW_FILE.items():
        if file_ext in file_extensions:
            cmd = view_cmd_associate % filename
            log.debug(u'Запуск комманды <%s>' % cmd)
            os.system(cmd)
    return True

