#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора месяца.
"""

import datetime
import wx
from . import std_dialogs_proto

__version__ = (0, 0, 1, 2)

TODAY = datetime.date.today()

# Диапазон списка годов
DEFAULT_YEAR_RANGE = 10

# Список годов
YEAR_LIST = [TODAY.year + i for i in range(-DEFAULT_YEAR_RANGE, DEFAULT_YEAR_RANGE)]


class icMonthDialog(std_dialogs_proto.monthDialogProto):
    """
    Диалоговое окно выбора месяца.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.monthDialogProto.__init__(self, *args, **kwargs)

        # Выбрать текущий месяц
        self.month_choice.Select(TODAY.month - 1)

        # Заполнить список годов
        self.year_choice.Clear()
        self.year_choice.AppendItems([str(n_year) for n_year in YEAR_LIST])

        # Выбрать текущий год
        self.year_choice.Select(YEAR_LIST.index(TODAY.year))

        self._selected_month = None

    def getSelectedMonth(self):
        return self._selected_month

    def getSelectedMonthAsDatetime(self):
        if self._selected_month:
            return datetime.datetime(year=self._selected_month[0], month=self._selected_month[1], day=1)
        return None

    def onCancelButtonClick(self, event):
        self._selected_month = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_month = (YEAR_LIST[self.year_choice.GetSelection()],
                                self.month_choice.GetSelection() + 1)
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

    dlg = icMonthDialog(frame)

    result = dlg.ShowModal()
    if result == wx.ID_OK:
        print((u'Selected month <%s> <%s>' % (dlg.getSelectedMonth(), dlg.getSelectedMonthAsDatetime())))

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
