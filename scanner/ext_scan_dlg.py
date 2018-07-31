#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнителные диалоговые окна управления сканированием.
"""

import os
import os.path
import wx

from ic.std.log import log
from ic.std.dlg import dlg
from ic.std.utils import execfunc
from ic.std.utils import pdf_func
from . import scanner_dlg_proto

__version__ = (0, 0, 1, 7)


class icLoadSheetsDialog(scanner_dlg_proto.icLoadSheetsDlgProto):
    """
    Диалоговое окно загрузки листов в лоток сканнера.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        scanner_dlg_proto.icLoadSheetsDlgProto.__init__(self, *args, **kwargs)

        self.real_sheet = 60

    def setMaxSheets(self, max_sheets=60):
        """
        Установить максимальное возможное количество листов для сканирования.
        @param max_sheets: Максимальное возможное количество листов для сканирования.
        """
        self.sheets_spinCtrl.SetRange(1, max_sheets)
        self.sheets_spinCtrl.SetValue(max_sheets)

    def getSheets(self):
        """
        Количество листов, выбранных пользователем для сканирования.
        @return: Количество листов, выбранных пользователем для сканирования.
        """
        return self.real_sheet

    def onNextButtonClick(self, event):
        """
        Обработчик кнопки <Далее>.
        """
        self.real_sheet = self.sheets_spinCtrl.GetValue()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.real_sheet = -1
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


class icVerifyScanDialog(scanner_dlg_proto.icVerifyScanDlgProto):
    """
    Диалоговое окно проверки результатов сканирования.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        scanner_dlg_proto.icVerifyScanDlgProto.__init__(self, *args, **kwargs)

        self.verify_filename = None

    def setVerifyFilename(self, filename):
        """
        Запомнить проверяемый файл.
        @param filename: Полное имя проверяемого файла.
        """
        self.verify_filename = filename

    def onPreviewButtonClick(self, event):
        """
        Обработчик кнопки <Предварительный просмотр...>.
        """
        execfunc.view_file_ext(self.verify_filename)
        event.Skip()

    def onReScanButtonClick(self, event):
        """
        Обработчик кнопки <Пересканировать>.
        """
        self.EndModal(wx.ID_BACKWARD)
        event.Skip()

    def onNextButtonClick(self, event):
        """
        Обработчик кнопки <Далее>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


def scan_glue_load_sheets(parent=None, max_sheets=60):
    """
    Определить количество листо для сканирования части.
    @param parent: Родительское окно.
    @param max_sheets: Максимально допустимое количество листов в лотке для сканирования.
    @return: Количество листов выбранных пользователем для сканированния.
        Либо -1, если просто ничего не выбрано или нажата <Отмена>.
    """
    dlg = icLoadSheetsDialog(parent=parent)
    dlg.setMaxSheets(max_sheets)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return dlg.getSheets()
    return -1


def scan_glue_verify(parent=None, verify_filename=None):
    """
    Процедура проверки результатов сканирования части.
    @param parent: Родительское окно.
    @param verify_filename: Полное имя проверяемого файла.
    @return: True - сканирование прошло удачно. Подтверждено пользователем.
        False - Сканирование отменено.
        None - Требуется пересканировать часть. Определено пользователем.
    """
    dlg = icVerifyScanDialog(parent=parent)
    dlg.setVerifyFilename(verify_filename)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return True
    elif result == wx.ID_BACKWARD:
        return None
    return False


def scan_glue_mode(scan_manager, scan_filename, n_sheets, is_duplex=False, max_tray_sheets=60):
    """
    Запуск режима склеивания документа по частям.
    @param scan_manager: Менеджер сканирования.
    @param scan_filename: Имя результирующего файла скана.
    @param n_sheets: Количество листов.
    @param is_duplex: Двустороннее сканирование?
    @param max_tray_sheets: Максимально допустимое количество листов в лотке сканера.
    @return: True/False.
    """
    # Основной цикл сканирования документа по частям и последующая склейка
    n_part = 1
    scan_file_path, scan_file_ext = os.path.splitext(scan_filename)
    part_suffix = '_part%03d' % n_part
    new_scan_filename = scan_file_path + part_suffix + scan_file_ext
    sheets = scan_glue_load_sheets(None, min(max_tray_sheets, n_sheets))
    scan_sheet_count = sheets
    is_cancel = scan_sheet_count <= 0

    while (0 < scan_sheet_count <= n_sheets) or is_cancel:
        log.debug(u'Сканирование файла <%s> Сканировать листов [%d]' % (new_scan_filename, sheets))
        # Если используется дуплекс, то надо увеличить количество страниц
        scan_n_pages = sheets * 2 if is_duplex else sheets
        # Запуск процесса сканирования
        scan_result = scan_manager.multiScan(new_scan_filename, scan_n_pages)
        if scan_result and os.path.exists(new_scan_filename):
            verify_result = scan_glue_verify(None, new_scan_filename)
            if verify_result:
                n_part += 1
                part_suffix = '_part%03d' % n_part
                new_scan_filename = scan_file_path + part_suffix + scan_file_ext
                do_scan_sheet_count =  min(max_tray_sheets, n_sheets-scan_sheet_count)
                if do_scan_sheet_count <= 0:
                    # Все листы отсканированны
                    break
                sheets = scan_glue_load_sheets(None, do_scan_sheet_count)
                if sheets <= 0:
                    # Нажата <Отмена>
                    is_cancel = True
                    break
                scan_sheet_count += sheets
            elif verify_result is None:
                scan_sheet_count -= sheets
                sheets = scan_glue_load_sheets(None, min(max_tray_sheets, n_sheets))
                if sheets <= 0:
                    # Нажата <Отмена>
                    is_cancel = True
                    break
                scan_sheet_count += sheets
            else:
                is_cancel = True
                log.warning(u'Сканирование по частям файла <%s> отменено' % new_scan_filename)
                break
        else:
            is_cancel = True
            log.warning(u'Ошибка сканирования файла <%s>' % new_scan_filename)

    # Склеить отсканированные части документа
    if not is_cancel:
        part_pdf_filenames = [scan_file_path + ('_part%03d' % i_part) + scan_file_ext for i_part in range(1, n_part)]
        log.debug(u'Объединение %d частей скана %s в PDF файл %s' % (n_part-1, part_pdf_filenames, scan_filename))
        glue_result = pdf_func.glue_pdf_files(scan_filename, *part_pdf_filenames)
        
        dlg.getMsgBox(u'СКАНИРОВАНИЕ', 
                      u'Загрузите в лоток сканера документы для последующего сканирования')
        return glue_result
    else:
        log.warning(u'Режим объединения сканированного документа по частям отменен')

    return False
