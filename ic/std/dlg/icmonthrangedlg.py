#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора периода по месяцам.
"""

import datetime
import wx
from . import std_dialogs_proto


class icMonthRangeDialog(std_dialogs_proto.monthRangeDialogProto):
    """
    Диалоговое окно выбора периода по месяцам.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.monthRangeDialogProto.__init__(self, *args, **kwargs)

        self._selected_range = None

    def getSelectedMonthRange(self):
        return self._selected_range

    def getSelectedMonthRangeAsDatetime(self):
        if self._selected_range:
            return (datetime.datetime(year=self._selected_range[0][0], month=self._selected_range[0][1], day=1),
                    datetime.datetime(year=self._selected_range[1][0], month=self._selected_range[1][1], day=1))
        return None

    def onCancelButtonClick(self, event):
        self._selected_range = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        first_selected_month = (self.yearFirstChoiceControl.get_selected_year(),
                                self.monthFirstChoiceControl.get_selected_month_num())
        last_selected_month = (self.yearLastChoiceControl.get_selected_year(),
                               self.monthLastChoiceControl.get_selected_month_num())
        self._selected_range = (first_selected_month, last_selected_month)
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

    dlg = icMonthRangeDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
