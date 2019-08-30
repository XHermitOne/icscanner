#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно календаря.
"""

import wx
from . import std_dialogs_proto
from ic.std.utils import timefunc

__version__ = (0, 1, 1, 1)


class icCalendarDialog(std_dialogs_proto.calendarDialogProto):
    """
    Диалоговое окно календаря.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.calendarDialogProto.__init__(self, *args, **kwargs)

        self._selected_date = None

    def getSelectedDate(self):
        return self._selected_date

    def getSelectedDateAsDatetime(self):
        return timefunc.wxdate2pydate(self._selected_date)

    def onCancelButtonClick(self, event):
        self._selected_date = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_date = self.calendarCtrl.GetDate()
        self.EndModal(wx.ID_OK)
        event.Skip()


def test():
    """
    Тестирование.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(0)

    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    dlg = icCalendarDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
