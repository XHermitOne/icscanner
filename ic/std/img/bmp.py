#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль управления файлами образов *.BMP, *.GIF, *.JPG и т.п.
"""

# Подключение библиотек
import os
import os.path
import wx

from ic.std.log import log


def getImageFileType(img_filename):
    """
    Определить тип файла образа по его расширению ( .jpg, ... ).
    @param img_filename: Полное имя файла.
    """
    if img_filename == '' or not os.path.exists(img_filename):
        log.warning('File <%s> not found' % img_filename)
        return None

    try:
        name, ext = os.path.splitext(img_filename)
        ext = ext[1:].upper()
        if ext == 'BMP':
            return wx.BITMAP_TYPE_BMP
        elif ext == 'GIF':
            return wx.BITMAP_TYPE_GIF
        elif ext == 'JPG' or ext == 'JPEG':
            return wx.BITMAP_TYPE_JPEG
        elif ext == 'PCX':
            return wx.BITMAP_TYPE_PCX
        elif ext == 'PNG':
            return wx.BITMAP_TYPE_PNG
        elif ext == 'PNM':
            return wx.BITMAP_TYPE_PNM
        elif ext == 'TIF' or ext == 'TIFF':
            return wx.BITMAP_TYPE_TIF
        elif ext == 'XBM':
            return wx.BITMAP_TYPE_XBM
        elif ext == 'XPM':
            return wx.BITMAP_TYPE_XPM
        else:
            log.warning('Not support image file type <%s>' % ext)
    except:
        log.error('Get image file type')

    return None


def createBitmap(img_filename, bMakeMask=False):
    """
    Создать объект Bitmap из файла ImgFileName_.
    @param img_filename: Имя файла.
    @param bMakeMask: Флаг создания маски по изображению.
        Фон д.б. CYAN (0, 255, 255)
    @return: Возвращает созданный объект или None в случае ошибки.
    """
    try:
        # Преобразовать относительные пути в абсолютные
        img_filename = os.path.abspath(os.path.normpath(img_filename))
        if not img_filename or not os.path.exists(img_filename):
            log.warning('File <%s> not found' % img_filename)
            return None

        bmp = wx.Bitmap(img_filename,getImageFileType(img_filename))
        if bMakeMask:
            # Создать маску и присоединить ее к битмапу
            phone_colour = wx.CYAN
            bmp.SetMask(wx.MaskColour(bmp, phone_colour))
        return bmp
    except:
        log.error(u'Ошибка создания образа файла <%s>' % img_filename)
        return None


def createEmptyBitmap(width, height, colour):
    """
    Создать пустой битмап.
    @param width, height: Размер битмапа.
    @param colour: Цвет фона.
    """
    try:
        # Пустой квадратик
        bmp = wx.EmptyBitmap(width, height)
        # Создать объект контекста устройства
        dc = wx.MemoryDC()
        # Выбрать объект для контекста
        dc.SelectObject(bmp)
        # Изменить фон
        dc.SetBackground(wx.Brush(colour))
        dc.Clear()
        # Освободить объект
        dc.SelectObject(wx.NullBitmap)
        return bmp
    except:
        log.error('Create empty bitmap SIZE: <%s, %s> COLOUR: <%s>' % (wodth, height, colour))
        return None
