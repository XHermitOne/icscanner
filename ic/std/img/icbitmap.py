#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import os
import wx
from ic.std.log import log

__version__ = (0, 0, 1, 2)

# Буфек картинок
icUserBitmapBuff = {}


def icBitmapType(filename):
    """
    Get the type of an image from the file's extension ( .jpg, etc. )
    """
    if filename == '':
        return None

    try:
        name, ext = os.path.splitext(filename)
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

    except:
        log.fatal(u'FILE ERROR:')

    return None


def GetUserBitmap(fileName, subsys, dir='images'):
    """
    Функция возвращает объект картинки из пользовательской библиотеки.
    
    @type subsys: C{string}
    @param subsys: Имя подсистемы в которой ищется картинка.
    @type fileName: C{string}
    @param fileName: Имя картинки.
    @rtype: C{wx.Bitmap}
    @return: Объект картинки.
    """
    global icUserBitmapBuff
    key = os.path.join(str(subsys), fileName)
    
    if key in icUserBitmapBuff:
        return icUserBitmapBuff[key]
    else:
        typ = icBitmapType(fileName)
        
        if typ:
            import ic.utils.resource as resource
            path = resource.icGetResPath().replace('\\', '/')
            if not subsys:
                path = '%s/%s/%s' % (path, dir, fileName)
            else:
                path = '%s/%s/%s/%s' % ('/'.join(path.split('/')[:-1]), subsys, dir, fileName)
                
            img = wx.Image(path, typ)
            bmp = img.ConvertToBitmap()
            icUserBitmapBuff[key] = bmp
            return bmp
