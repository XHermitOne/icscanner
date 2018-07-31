#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Библиотека функций определения режима работы движка.
@author: Шурик Колчанов.
"""

from ic import config

# --- Константы ---
# Режим работы движка True-режим выполнения
global RUNTIME_MODE
RUNTIME_MODE = True

# Режим работы с БД
global DB_MODE
DB_MODE = None

# Режим работы с БД
DB_MONOPOLY = '-m'
DB_SHARE = '-s'

# --- Функции ---


def isRuntimeMode():
    """
    Движок запущен?
    """
    global RUNTIME_MODE
    return RUNTIME_MODE


def setRuntimeMode(RuntimeMode_=True):
    """
    Установить признак режима исполнения.
    """
    global RUNTIME_MODE
    RUNTIME_MODE = RuntimeMode_


def getDBMode():
    """
    Режим работы с БД.
    """
    global DB_MODE
    return DB_MODE


def setDBMode(DBMode_=DB_SHARE):
    """
    Устаонвить режим работы с БД.
    """
    global DB_MODE
    DB_MODE = DBMode_


def isDebugMode():
    """
    Режим отладки.
    """
    return config.DEBUG_MODE
