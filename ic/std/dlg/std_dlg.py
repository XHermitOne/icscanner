#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции стандартных диалогов прикладного уровня.
"""

import wx
import wx.lib.calendar

try:
    from . import iccalendardlg
except ImportError:
    pass

from . import icyeardlg
from . import icmonthdlg
from . import icmonthrangedlg
try:
    from . import icdaterangedlg
except ImportError:
    pass

from . import icnsilistdlg

__version__ = (0, 1, 1, 2)


def getDateDlg(parent=None):
    """
    Выбор даты в диалоговом окне календаря.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Выбранную дату(datetime) или None если нажата <отмена>.
    """
    selected_date = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = iccalendardlg.icCalendarDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_date = dlg.getSelectedDateAsDatetime()
    dlg.Destroy()

    return selected_date


def getYearDlg(parent=None):
    """
    Выбор года в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Выбранный год (datetime) или None если нажата <отмена>.
    """
    selected_year = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icyeardlg.icYearDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_year = dlg.getSelectedYearAsDatetime()
    dlg.Destroy()

    return selected_year


def getMonthDlg(parent=None):
    """
    Выбор месяца в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Выбранный месяц (datetime) или None если нажата <отмена>.
    """
    selected_month = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icmonthdlg.icMonthDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_month = dlg.getSelectedMonthAsDatetime()
    dlg.Destroy()

    return selected_month


def getMonthRangeDlg(parent=None):
    """
    Выбор периода по месяцам в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Кортеж периода по месяцам (datetime) или None если нажата <отмена>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icmonthrangedlg.icMonthRangeDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedMonthRangeAsDatetime()
    dlg.Destroy()

    return selected_range


def getDateRangeDlg(parent=None):
    """
    Выбор периода по датам в диалоговом окне.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @return: Кортеж периода по датам (datetime) или None если нажата <отмена>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icdaterangedlg.icDateRangeDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedDateRangeAsDatetime()
    dlg.Destroy()

    return selected_range


def getNSIListDlg(parent=None,
                  db_url=None, nsi_sprav_tabname=None,
                  code_fieldname='cod', name_fieldname='name',
                  ext_filter=''):
    """
    Выбор значения из простого спискового справочника.
    @param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    @param db_url: URL подключения к БД.
    @param nsi_sprav_tabname: Имя таблицы справочника.
    @param code_fieldname: Имя поля кода в таблице справочника.
    @param name_fieldname: Имя поля наименования в таблице справочника.
    @param ext_filter: Дополнительный фильтр записей.
    @return: Выбранный код справочника или None если нажата <отмена>.
    """
    selected_code = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icnsilistdlg.icNSIListDialog(parent)
    dlg.Centre()
    dlg.setDbURL(db_url)
    dlg.initChoice(nsi_sprav_tabname, code_fieldname, name_fieldname, ext_filter)

    if dlg.ShowModal() == wx.ID_OK:
        selected_code = dlg.getSelectedCode()

    try:
        dlg.Destroy()
    except wx.PyDeadObjectError:
        print(u'wx.PyDeadObjectError. Ошибка удаления диалогового окна')
    return selected_code


def getStdDlgQueue(*dlgs):
    """
    Определить очередность вызова диалоговых окон для
    определения параметров запроса отчета.
    @param dlgs: Список словарей описания вызова диалоговых окон.
        Вызов диалогового окна - это словарь формата:
        {'key': Ключ результата,
         'func': Функция вызова диалога,
         'args': Список аргументов функции вызова диалога,
         'kwargs': Словарь именованных аргументов вункции вызова диалога}.
    @return: Словарь заполненных значений с помощью диалоговых функций.
    """
    # ВНИМАНИЕ! Для корректного отображения окон необходимо указать
    # frame в явном виде
    frame = wx.Frame(None, -1)
    frame.Center()

    result = dict()

    for dlg in dlgs:
        dlg_func = dlg.get('func', None)
        args = dlg.get('args', tuple())
        kwargs = dlg.get('kwargs', dict())
        if dlg_func:
            result_key = dlg['key'] if 'key' in dlg else dlg_func.__name__
            result[result_key] = dlg_func(parent=frame, *args, **kwargs)

    frame.Destroy()
    return result


def test():
    """
    Тестирование.
    """
    app = wx.PySimpleApp()
    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    print((getDateDlg(frame)))

    frame.Destroy()

    app.MainLoop()


def test_nsi_1():
    """
    Тестирование.
    """
    app = wx.PySimpleApp()
    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    # Параметры подключения к БД
    DB_HOST = '10.0.0.3'
    DB_PORT = 5432
    DB_USER = 'xhermit'
    DB_PASSWORD = 'xhermit'
    DB_NAME = 'testing'

    DB_URL = 'postgres://%s:%s@%s:%d/%s' % (DB_USER, DB_PASSWORD,
                                            DB_HOST, DB_PORT, DB_NAME)

    print((getNSIListDlg(frame, db_url=DB_URL,
                        nsi_sprav_tabname='nsi_tags')))

    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test_nsi_1()
