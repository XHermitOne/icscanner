#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора значения из простого спискового справочника.
"""

import wx
import sqlalchemy
from . import std_dialogs_proto

__version__ = (0, 1, 1, 1)

SQL_TEMPLATE = '''
SELECT DISTINCT
    %s AS cod,
    %s AS name
FROM
    public.%s
%s;
'''


class icNSIListDialog(std_dialogs_proto.NSIListDialogProto):
    """
    Диалоговое окно выбора значения из простого спискового справочника.
    @param nsi_codes: Список кодов справочника.
    @param selected_code: Выбранный код справочника.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.NSIListDialogProto.__init__(self, *args, **kwargs)

        self.db_url = None

        # Коды справочника
        self.nsi_codes = list()
        # Выбранный код справочника
        self.selected_code = None

    def setDbURL(self, db_url):
        """
        Установить URL связи с БД.
        @param db_url: URL связи с БД.
        """
        self.db_url = db_url

    def connect(self, db_url=None):
        """
        Установить связь с БД.
        @param db_url: URL связи с БД.
        @return: Объект связи с БД.
        """
        if db_url is None:
            db_url = self.db_url
        connection = sqlalchemy.create_engine(db_url, echo=True)
        return connection

    def disconnect(self, connection=None):
        """
        Разорвать соединение с БД.
        @param connection: Объект связи с БД.
        @return: True / False.
        """
        if connection:
            connection.dispose()
            connection = None
            return True
        return False

    def getDataset(self, tabname,
                   code_fieldname='cod', name_fieldname='name',
                   ext_filter=''):
        """
        Получить датасет для просмотра.
        @param tabname: Имя таблицы справочника.
        @param code_fieldname: Имя поля кода в таблице справочника.
        @param name_fieldname: Имя поля наименования в таблице справочника.
        @param ext_filter: Дополнительный фильтр записей.
        @return: Возвращает список словарей записей.
        """
        connection = self.connect()

        ext_filter = 'WHERE %s' % ext_filter if ext_filter else ''
        sql = SQL_TEMPLATE % (code_fieldname, name_fieldname, tabname, ext_filter)

        # Фильтруется SQL выражением
        recordset = connection.execute(sql).fetchall()
        result = [dict(record) for record in recordset]

        self.disconnect(connection)
        return result

    def initChoice(self, tabname,
                   code_fieldname='cod', name_fieldname='name',
                   ext_filter=''):
        """
        Инициализация списка выбора диалогового окна.
        @param tabname: Имя таблицы справочника.
        @param code_fieldname: Имя поля кода в таблице справочника.
        @param name_fieldname: Имя поля наименования в таблице справочника.
        @param ext_filter: Дополнительный фильтр записей.
        @return: True/False.
        """
        dataset = self.getDataset(tabname, code_fieldname, name_fieldname, ext_filter)
        self.nsi_codes = [rec['cod'] for rec in dataset]
        choices = [rec['name'] for rec in dataset]
        for item in choices:
            self.nsi_listBox.Append(item)

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.selected_code = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        idx = self.nsi_listBox.GetSelection()
        if idx >= 0:
            self.selected_code = self.nsi_codes[idx]
        else:
            self.selected_code = None

        self.EndModal(wx.ID_OK)
        event.Skip()

    def getSelectedCode(self):
        return self.selected_code
