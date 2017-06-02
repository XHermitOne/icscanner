#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора периода по датам.
"""

import wx
from . import std_dialogs_proto
from ic.std.utils import ic_time


class icDateRangeDialog(std_dialogs_proto.dateRangeDialogProto):
    """
    Диалоговое окно выбора периода по датам.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.dateRangeDialogProto.__init__(self, *args, **kwargs)

        self._selected_range = None

    def getSelectedDateRange(self):
        return self._selected_range

    def getSelectedDateRangeAsDatetime(self):
        if self._selected_range:
            return ic_time.wxdate2pydate(self._selected_range[0]), ic_time.wxdate2pydate(self._selected_range[1])
        return None

    def onCancelButtonClick(self, event):
        self._selected_range = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_range = (self.firstDatePicker.GetValue(),
                                self.lastDatePicker.GetValue())
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

    dlg = icDateRangeDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
