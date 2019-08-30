#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя.
"""

# Подключение пакетов
import os
import os.path

import wx
import wx.lib.imagebrowser

__version__ = (0, 0, 1, 3)


# ДИАЛОГОВЫЕ ФУНКЦИИ
def getFileDlg(parent=None, title='', wildcard='', default_path=''):
    """
    Открыть диалог выбора файла для открытия/записи.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param wildcard: Фильтр файлов.
    @param default_path: Путь по умолчанию.
    @return: Возвращает полное имя выбранного файла.
    """
    result = ''
    dlg = None
    win_clear = False

    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        wildcard += '|All Files (*.*)|*.*'
        dlg = wx.FileDialog(parent, title, '', '', wildcard, wx.OPEN)
        if default_path:
            dlg.SetDirectory(os.path.normpath(default_path))
        else:
            dlg.SetDirectory(os.getcwd())

        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPaths()[0]
        else:
            result = ''
        dlg.Destroy()
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return result


def getDirDlg(parent=None, title='', default_path=''):
    """
    Диалог выбора каталога.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param default_path: Путь по умолчанию.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        dlg = wx.DirDialog(parent, title, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        # Установка пути по умолчанию
        if not default_path:
            default_path = os.getcwd()
        dlg.SetPath(default_path)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPath()
        else:
            result = ''
    finally:
        dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return result


def getImageDlg(parent=None, default_img_dir=None):
    """
    Диалог выбора графических файлов.
    @param parent: Ссылка на окно.
    @param default_img_dir: Указание папки образа.
    @return: Возвращает полное имя выбранного файла.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        # Определить папку образов
        if not default_img_dir or not os.path.exists(default_img_dir):
            default_img_dir = os.getcwd()
        # Диалоговое окно выбора образа
        dlg = wx.lib.imagebrowser.ImageDialog(parent, default_img_dir)
        dlg.CenterOnScreen()

        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetFile()

    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
        
    return result


def getColorDlg(parent=None, title='', default=wx.BLACK):
    """
    Диалог выбора цвета
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param default: Значение по умолчанию.
    @return: Возвращает выбранный цвет или default.
    """
    result = (0, 0, 0)
    dlg = None
    win_clear = False
    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        dlg = wx.ColourDialog(parent, wx.ColourData().SetColour(default))
        dlg.SetTitle(title)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetColourData().GetColour()
        else:
            result = default
    finally:
        dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return result


def getTextInputDlg(parent=None, title='', message='', default=''):
    """
    Диалог ввода строки.
    @param parent: Ссылка на окно.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @param default: Значение по умолчанию.
    @return: Возвращает введеную строку, если нажата отмена, то пустую строку.
    """
    result = ''
    dlg = None
    win_clear = False
    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        dlg = wx.TextEntryDialog(parent, message, title)
        if default is None:
            default = ''
        dlg.SetValue(default)
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetValue()
            return txt
    finally:
        dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return result


def getAskDlg(title='', message='', style=wx.YES_NO | wx.ICON_QUESTION):
    """
    Диалог вопроса.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @param style: Стиль диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(message, title, style)
    except:
        raise


def getAskBox(*args, **kwargs):
    """
    Диалог вопроса.
    """
    return getAskDlg(*args, **kwargs) == wx.YES


def getMsgBox(title='', message='', parent=None):
    """
    Вывод сообщения.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(message, title, wx.OK, parent)
    except:
        raise


def getErrBox(title='', message='', parent=None):
    """
    Вывод сообщения об ошибке.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR, parent)
    except:
        raise


def getWarningBox(title='', message='', parent=None):
    """
    Вывод предупреждающего сообщения.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @return: Код нажатой кнопки (Например: wx.YES или wx.NO).
    """
    try:
        return wx.MessageBox(message, title, wx.OK | wx.ICON_WARNING, parent)
    except:
        raise


def getSingleChoiceDlg(parent=None, title='', message='', choice=None):
    """
    Диалог выбора.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @return: Выбранный текст или None, если нажата Cancel.
    """
    result = None
    dlg = None
    win_clear = False
    if choice is None:
        choice = []
    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        dlg = wx.SingleChoiceDialog(parent, message, title, choice, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetStringSelection()
            return txt
    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()

    return result


def getSingleChoiceIdxDlg(parent=None, title='', message='', choice=None):
    """
    Диалог выбора.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param message: Текст диалога.
    @param choice: Список выбора. Список строк.
    @return: Выбранный индекс в списке выбора или -1, если нажата Cancel.
    """
    idx = -1
    dlg = None
    win_clear = False
    if choice is None:
        choice = []
    try:
        if parent is None:
            parent = wx.Frame(None, -1, '')
            win_clear = True

        dlg = wx.SingleChoiceDialog(parent, message, title, choice, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()

    finally:
        if dlg:
            dlg.Destroy()
        # Удаляем созданное родительское окно
        if win_clear:
            parent.Destroy()
    return idx
