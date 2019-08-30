#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора года.
"""

import datetime
import wx
from . import std_dialogs_proto

__version__ = (0, 1, 1, 1)


class icYearDialog(std_dialogs_proto.yearDialogProto):
    """
    Диалоговое окно выбора года.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.yearDialogProto.__init__(self, *args, **kwargs)

        self._selected_year = None

    def getSelectedYear(self):
        return self._selected_year

    def getSelectedYearAsDatetime(self):
        if self._selected_year:
            return datetime.datetime(year=self._selected_year, month=1, day=1)
        return None

    def onCancelButtonClick(self, event):
        self._selected_year = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_year = self.yearChoiceControl.get_selected_year()
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

    dlg = icYearDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
