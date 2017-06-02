#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль сервисных функций программиста перенесены из ic.utils.ic_util.py
"""

from ic.std.log import log

__version__ = (0, 0, 1, 2)


def ReCodeString(String_, StringCP_, NewCP_='utf-8'):
    """
    Перекодировать из одной кодировки в другую.
    @param String_: Строка.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    """
    if NewCP_.upper() == 'UNICODE':
        # Кодировка в юникоде.
        return unicode(String_, StringCP_)

    if NewCP_.upper() == 'OCT' or NewCP_.upper() == 'HEX':
        # Закодировать строку в восьмеричном/шестнадцатеричном виде.
        return icOctHexString(String_, NewCP_)

    string = unicode(String_, StringCP_)
    return string.encode(NewCP_)


def icOctHexString(String_, Code_):
    """
    Закодировать строку в восьмеричном/шестнадцатеричном виде.
        Символы с кодом < 128 не кодируются.
    @param String_:
    @param Code_: Кодировка 'OCT'-восьмеричное представление.
                            'HEX'-шестнадцатеричное представление.
    @return: Возвращает закодированную строку.
    """
    try:
        if Code_.upper() == 'OCT':
            fmt = '\\%o'
        elif Code_.upper() == 'HEX':
            fmt = '\\x%x'
        else:
            # Ошибка аргументов
            log.warning(u'Функция icOctHexString: Ошибка аргументов.')
            return None
        # Перебор строки по символам
        ret_str = ''
        for char in String_:
            code_char = ord(char)
            # Символы с кодом < 128 не кодируются.
            if code_char > 128:
                ret_str += fmt % code_char
            else:
                ret_str += char
        return ret_str
    except:
        log.fatal()
        return None
