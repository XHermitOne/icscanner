#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно управления сканированием.
"""

import os
import os.path
import shutil
import wx

from ic.std.log import log
from ic.std.utils import ini
from ic.std.utils import ic_file
from ic.std.utils import execfunc
from ic.std.dlg import dlg
from ic import config
from . import scanner_dlg_proto
from . import scan_manager

__version__ = (1, 1, 2, 1)


class icScanOptions:
    """
    Класс управления опциями сканирования. 
    """
    def __init__(self):
        """
        Конструктор.
        """
        self.opt_filename = None

        # Опции сканирования
        self.scanner = None
        self.scan_source = None
        self.scan_mode = None
        self.is_multi_scan = False
        self.is_preview = False
        self.page_size = None
        self.scan_area = None
        self.scan_dir = None
        self.scan_filename = None
        self.scan_filetype = None
        self.depth = None
        self.ext_scan_cmd = None

        self.loadOptions()

    def genOptFileName(self):
        """
        Генерация имени файла параметров.
        """
        if self.opt_filename is None:
            self.opt_filename = config.DEFAULT_OPTIONS_FILENAME
        return self.opt_filename

    def loadOptions(self, sFileName=None):
        """
        Загрузить параметры сканирования из конфигурационного файла.
        @param sFileName: Имя файла параметров.
        """
        if sFileName is None:
            sFileName = self.genOptFileName()

        ini_dict = ini.INI2Dict(sFileName)
        if ini_dict:
            self.setExtOptions(**ini_dict['SCAN_OPTIONS'])
        else:
            log.warning(u'Параметры сканирования не загружены из конфигурационного файла')

    def saveOptions(self, sFileName=None):
        """
        Записать параметры сканирования в конфигурационный файл.
        @param sFileName: Имя файла параметров.
        """
        if sFileName is None:
            sFileName = self.genOptFileName()

        ini_dict = dict()
        ini_dict['SCAN_OPTIONS'] = dict()
        ini_dict['SCAN_OPTIONS']['scanner'] = self.scanner
        ini_dict['SCAN_OPTIONS']['source'] = self.scan_source
        ini_dict['SCAN_OPTIONS']['mode'] = self.scan_mode
        ini_dict['SCAN_OPTIONS']['is_multi_scan'] = self.is_multi_scan
        ini_dict['SCAN_OPTIONS']['is_preview'] = self.is_preview
        ini_dict['SCAN_OPTIONS']['page-size'] = self.page_size
        ini_dict['SCAN_OPTIONS']['area'] = self.scan_area
        ini_dict['SCAN_OPTIONS']['scan_dir'] = self.scan_dir
        ini_dict['SCAN_OPTIONS']['file_name'] = self.scan_filename
        ini_dict['SCAN_OPTIONS']['file_type'] = self.scan_filetype
        ini_dict['SCAN_OPTIONS']['depth'] = self.depth
        ini_dict['SCAN_OPTIONS']['ext_scan_cmd'] = self.ext_scan_cmd

        ini.Dict2INI(ini_dict, sFileName)
        
    def setExtOptions(self, **options):
        """
        Установить дополнительные опции.
        @param options: Словарь опций.
        """
        log.debug(u'Опции сканирования: %s' % options)
        if options:
            if 'scanner' in options:
                self.scanner = options.get('scanner', None)
            if 'source' in options:
                self.scan_source = options.get('source', None)
            if 'mode' in options:
                self.scan_mode = options.get('mode', None)
            if 'is_multi_scan' in options:
                self.is_multi_scan = options.get('is_multi_scan', None)
            if 'is_preview' in options:
                self.is_preview = options.get('is_preview', None)
            if 'page_size' in options:
                self.page_size = options.get('page_size', None)
            if 'area' in options:
                self.scan_area = options.get('area', None)
            if 'scan_dir' in options:
                self.scan_dir = options.get('scan_dir', None)
            if 'file_name' in options:
                self.scan_filename = options.get('file_name', None)
            if 'file_type' in options:
                self.scan_filetype = options.get('file_type', None)
            if 'depth' in options:
                self.depth = options.get('depth', None)
            if 'ext_scan_cmd' in options:
                self.ext_scan_cmd = options.get('ext_scan_cmd', None)
        else:
            log.warning(u'Не определены опции сканирования для установки')


class icScanAdministrator(icScanOptions):
    """
    Промежуточный класс управления менеджером сканирования.
    """
    def __init__(self):
        """
        Конструктор.
        """
        icScanOptions.__init__(self)

        self.scan_manager = scan_manager.icScanManager()
        self.scan_manager.init()

    def getScanManager(self):
        """
        Менеджер сканирования.
        @return: объект менеджера сканирования.
        """
        if hasattr(self, 'scan_manger'):
            return self.scan_manager
        return None

    def runScan(self):
        """
        Запусть процесс сканирования,
        согласно выставленным параметрам.
        @return: True/False
        """
        try:
            return self._runScan()
        except:
            log.fatal(u'Ошибка сканирования')
        return False
            
    def _runScan(self):
        """
        Запусть процесс сканирования,
        согласно выставленным параметрам.
        @return: True/False
        """
        if self.scan_manager is None:
            log.warning(u'Не определен менеджер сканирования')
            return False
        if self.scanner is None:
            log.warning(u'Не определено устройство сканирования')
            return False

        self.scan_manager.init()

        self.scan_manager.open(self.scanner)

        # Выставить все опции
        options = dict()
        if self.scan_source:
            options['source'] = self.scan_source
        if self.scan_mode:
            options['mode'] = self.scan_mode
        if self.depth:
            options['depth'] = self.depth
        if self.page_size:
            options['page_width'] = self.page_size[0]
            options['page_height'] = self.page_size[1]
        else:
            # ВНИМАНИЕ! Если не определить размер страницы
            # край скана будет обрезаться
            # По умолчанию A4 портретной ориентации
            options['page_width'] = 210.0
            options['page_height'] = 297.0
        if self.scan_area:
            options['tl_x'] = self.scan_area[0]
            options['tl_y'] = self.scan_area[1]
        if self.scan_area and self.page_size:
            options['br_x'] = self.page_size[0] - self.scan_area[2]
            options['br_y'] = self.page_size[1] - self.scan_area[3]
        else:
            # ВНИМАНИЕ! Если не определить размер страницы
            # край скана будет обрезаться
            # По умолчанию A4 портретной ориентации
            options['br_x'] = 210.0
            options['br_y'] = 297.0
            
        self.scan_manager.setScanOptions(**options)

        # Определение имени файла сканирования
        scan_filename = os.path.join(ic_file.getHomeDir(),
                                     config.PROFILE_DIRNAME,
                                     self.scan_filename+'.'+self.scan_filetype) if self.scan_filename else config.DEFAULT_SCAN_FILENAME
        if os.path.exists(scan_filename):
            # Удалить старый файл сканирования
            try:
                os.remove(scan_filename)
                log.info(u'Удален файл <%s>' % scan_filename)
            except OSError:
                log.fatal(u'Ошибка удаления файла <%s>' % scan_filename)
        log.debug(u'Сканирование в файл <%s>' % scan_filename)

        try:
            if not self.is_multi_scan:
                result = self.scan_manager.singleScan(scan_filename)
            else:
                result = self.scan_manager.multiScan(scan_filename)

            if not result:
                # Какая-то ошибка сканирования
                dlg.getErrBox(u'ОШИБКА',
                              u'Ошибка сканирования. Проверте листы в лотке сканера')
                return False

            if self.scan_dir:
                self.copyToScanDir(scan_filename, self.scan_dir)

            if self.is_preview:
                self.previewScanFile(scan_filename)
            return True
        except:
            log.fatal(u'Ошибка сканирования')
        return False

    def pages2sheets(self, page_count, is_duplex=False):
        """
        Перевод количества страниц в количество листов.
        @param page_count: Количество страниц.
        @param is_duplex: Двустороннее сканирование?
        @return: Количество листов.
        """
        if not is_duplex:
            # Если нет двустороннего сканирования,
            # то количество страниц совпадает с количеством листов
            return page_count
        else:
            # При двустороннем сканировании:
            return page_count / 2

    def runScanPack(self, *scan_filenames):
        """
        Запусть процесс сканирования в режиме пакетной обработки,
        согласно выставленным параметрам.
        @param scan_filenames: Имена файлов скана с указанием количества листов
            и признака 2-стороннего сканирования.
            Например:
                (scan001, 3, True), (scan002, 1, False), (scn003, 2, True), ...
        @return: True/False
        """
        if self.scan_manager is None:
            log.warning(u'Не определен менеджер сканирования')
            return False
        if self.scanner is None:
            log.warning(u'Не определено устройство сканирования')
            return False

        self.scan_manager.init()
        self.scan_manager.open(self.scanner)

        # Выставить все опции
        options = dict()
        if self.scan_source:
            options['source'] = self.scan_source
        if self.scan_mode:
            options['mode'] = self.scan_mode
        if self.depth:
            options['depth'] = self.depth
        if self.page_size:
            options['page_width'] = self.page_size[0]
            options['page_height'] = self.page_size[1]
        else:
            # ВНИМАНИЕ! Если не определить размер страницы
            # край скана будет обрезаться
            # По умолчанию A4 портретной ориентации
            options['page_width'] = 210.0
            options['page_height'] = 297.0
        if self.scan_area:
            options['tl_x'] = self.scan_area[0]
            options['tl_y'] = self.scan_area[1]
        if self.scan_area and self.page_size:
            options['br_x'] = self.page_size[0] - self.scan_area[2]
            options['br_y'] = self.page_size[1] - self.scan_area[3]
        else:
            # ВНИМАНИЕ! Если не определить размер страницы
            # край скана будет обрезаться
            # По умолчанию A4 портретной ориентации
            options['br_x'] = 210.0
            options['br_y'] = 297.0
            
        self.scan_manager.setScanOptions(**options)

        scans = [(os.path.join(ic_file.getHomeDir(),
                               config.PROFILE_DIRNAME,
                               scan_filename+'.'+self.scan_filetype) if scan_filename else config.DEFAULT_SCAN_FILENAME,
                  int(n_pages), bool(is_duplex)) for scan_filename, n_pages, is_duplex in scan_filenames]
        for scan_filename, n_pages, is_duplex in scans:
            full_scan_filename = os.path.join(os.environ.get('HOME', '/home/user'),
                                              config.PROFILE_DIRNAME,
                                              scan_filename)
            if os.path.exists(full_scan_filename):
                # Удалить старый файл сканирования
                try:
                    os.remove(full_scan_filename)
                    log.info(u'Удален ранее отсканированный файл <%s>' % full_scan_filename)
                except OSError:
                    log.fatal(u'Ошибка удаления файла <%s>' % full_scan_filename)

        try:
            scan_filenames = self.scan_manager.scan_pack(scan_filenames=scans)

            # Перенос отсканированных файлов в результирующую папку
            if self.scan_dir and os.path.exists(self.scan_dir):
                for scan_filename in scan_filenames:
                    if scan_filename and os.path.exists(scan_filename):
                        log.debug(u'Перенос файла <%s> в результирующую папку <%s>' % (scan_filename, self.scan_dir))
                        self.copyToScanDir(scan_filename, self.scan_dir)
                    else:
                        log.warning(u'Не определен результирующий файл сканирования')
            else:
                log.warning(u'Не определена результирующая папка сканирования')
                        
            return True
        except:
            log.fatal(u'Ошибка сканирования в режиме пакетной обработки')

        return False

    def copyToScanDir(self, scan_filename=None, scan_dir=None, doRemove=True):
        """
        Копировать файл - результат сканирования в папку.
        @param scan_filename: Результирующий файл сканирования.
            Если не указан, то берется файл по умолчанию.
        @param scan_dir: Папка сканирования.
        @param doRemove: Произвести перенос файла?
        @return: True/False
        """
        if scan_filename is None:
            scan_filename = config.DEFAULT_SCAN_FILENAME

        if scan_dir is None:
            scan_dir = self.scan_dir

        if not os.path.exists(scan_filename):
            log.warning(u'Не существует файл скана <%s>' % scan_filename)
            return False

        if scan_dir:
            if not os.path.exists(scan_dir):
                try:
                    os.makedirs(scan_dir)
                    log.info(u'Создана папка сканирования <%s>' % scan_dir)
                except OSError:
                    log.fatal(u'Ошибка создания папки сканирования <%s>' % scan_dir)
                    return False

            new_filename = os.path.join(scan_dir,
                                        os.path.basename(scan_filename))
            if scan_filename != new_filename:
                shutil.copyfile(scan_filename, new_filename)
                log.info(u'Копирование файла <%s> в директорию <%s>' % (scan_filename, scan_dir))
                if doRemove:
                    try:
                        os.remove(scan_filename)
                        log.info(u'Удален файл <%s>' % scan_filename)
                    except:
                        log.fatal(u'Ошибка удаления файла <%s>' % scan_filename)
            return True
        else:
            log.warning(u'Не определена папка сканирования')
        return False

    def runExtScan(self):
        """
        Запуск внешнего инструмента сканирования.
        @return: True/False.
        """
        if self.ext_scan_cmd:
            log.info(u'Запуск комманды <%s>' % self.ext_scan_cmd)
            os.system(self.ext_scan_cmd)
            return True
        return False

    def previewScanFile(self, scan_filename=None):
        """
        Просмотр результат сканирования.
        @param scan_filename: Результирующий файл сканирования.
            Если не указан, то берется файл по умолчанию.
        @return: True/False.
        """
        if scan_filename is None:
            scan_filename = config.DEFAULT_SCAN_FILENAME
        # Возможно файл после сканирования был уже перенесен в результирующую
        # папку поэтому просматривать необходимо файл в папке сканирования
        if not os.path.exists(scan_filename):
            scan_filename = os.path.join(self.scan_dir if self.scan_dir else config.PROFILE_PATH,
                                         os.path.basename(scan_filename))

        return execfunc.view_file_ext(scan_filename)


class icScannerDlg(scanner_dlg_proto.icScannerDlgProto,
                   icScanAdministrator):
    """
    Диалоговое окно управления сканированием.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        scanner_dlg_proto.icScannerDlgProto.__init__(self, *args, **kwargs)
        icScanAdministrator.__init__(self)

        self.init_ctrl()
        self.showOptions()

    def onInitDlg(self, event):
        """
        Инициализация диалога.
        """
        event.Skip()

    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        if self.scan_manager.isDevices():
            self.initComboBoxScanners()

        # Список источников
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'scanner--arrow.png'))
        self.source_comboBox.Append(u'Планшет', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document--arrow.png'))
        self.source_comboBox.Append(u'Фронтальная сторона', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'arrow-continue-180-top.png'))
        self.source_comboBox.Append(u'Обратная сторона', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'documents.png'))
        self.source_comboBox.Append(u'Дуплекс/Двустороннее сканирование', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.source_comboBox.SetSelection(0)

        # Список размера страницы
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document-number-4.png'))
        self.pagesize_comboBox.Append(u'A4', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document-number-3.png'))
        self.pagesize_comboBox.Append(u'A3', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.pagesize_comboBox.SetSelection(0)

        # Список форматов файлов сканов
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_pdf.png'))
        self.fileext_comboBox.Append(u'PDF', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_jpeg.png'))
        self.fileext_comboBox.Append(u'JPEG', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_jpg.png'))
        self.fileext_comboBox.Append(u'JPG', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_tif.png'))
        self.fileext_comboBox.Append(u'TIF', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_bmp.png'))
        self.fileext_comboBox.Append(u'BMP', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.fileext_comboBox.SetSelection(0)

        # Список режимов
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'border-weight.png'))
        self.mode_comboBox.Append(u'Штриховой', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'contrast.png'))
        self.mode_comboBox.Append(u'Полутоновой', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'gradient.png'))
        self.mode_comboBox.Append(u'Черно-белый', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'color.png'))
        self.mode_comboBox.Append(u'Цветной', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.mode_comboBox.SetSelection(2)

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'page.png'))
        bitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        self.m_bitmap1.SetBitmap(bitmap)

        option_notebookImageSize = wx.Size(16, 16)
        option_notebookIndex = 0
        option_notebookImages = wx.ImageList(option_notebookImageSize.GetWidth(), option_notebookImageSize.GetHeight())
        self.option_notebook.AssignImageList(option_notebookImages)

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'scanner.png'))
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if option_notebookBitmap.IsOk():
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document_spacing.png'))
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if option_notebookBitmap.IsOk():
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'property-blue.png'))
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if option_notebookBitmap.IsOk():
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        filename = os.path.splitext(os.path.basename(config.DEFAULT_SCAN_FILENAME))[0] if not self.scan_filename else self.scan_filename
        self.filename_textCtrl.SetValue(filename)

        self.depth_spinCtrl.SetValue(scan_manager.DEFAULT_DEPTH)
        # Внешний инструмент сканирования
        self.extern_cmd_textCtrl.SetValue(config.DEFAULT_EXT_SCAN_PRG)

        self.ok_button.SetFocus()

    def showOptions(self):
        """
        Выставить параметры сканирования в контролах окна.
        """
        if self.scanner:
            self.scanner_comboBox.SetStringSelection(self.scanner)

        if self.scan_source:
            i = 0
            try:
                log.debug(u'Установка источника сканирования <%s>' % self.scan_source)
                i = scan_manager.SCAN_SOURCES.index(self.scan_source)
            except ValueError:
                log.warning(u'Не найден источник сканирования <%s>' % self.scan_source)
            self.source_comboBox.Select(i)

        if self.scan_mode:
            i = 0
            try:
                i = scan_manager.SCAN_MODES.index(self.scan_mode)
            except ValueError:
                log.warning(u'Не найден режим сканирования <%s>' % self.scan_mode)
            self.mode_comboBox.Select(i)

        self.multiscan_checkBox.SetValue(bool(self.is_multi_scan))
        self.preview_checkBox.SetValue(bool(self.is_preview))

        if self.page_size:
            i = 0
            try:
                i = scan_manager.SCAN_PAGE_SIZES.index(self.page_size)
            except ValueError:
                log.warning(u'Не найден размер страницы сканирования <%s>' % self.page_size)
            self.pagesize_comboBox.Select(i)

        if self.scan_area:
            self.left_spinCtrl.SetValue(self.scan_area[0])
            self.top_spinCtrl.SetValue(self.scan_area[1])
            self.right_spinCtrl.SetValue(self.scan_area[2])
            self.bottom_spinCtrl.SetValue(self.scan_area[3])

        if self.scan_dir:
            self.scan_dirPicker.SetPath(self.scan_dir)

        if self.scan_filename:
            self.filename_textCtrl.SetValue(self.scan_filename)

        if self.scan_filetype:
            i = 0
            try:
                i = scan_manager.SCAN_FILE_TYPES.index(self.scan_filetype)
            except ValueError:
                log.warning(u'Не найден тип файла сканирования <%s>' % self.scan_filetype)
            self.fileext_comboBox.Select(i)

        if self.depth:
            self.depth_spinCtrl.SetValue(self.depth)

        if self.ext_scan_cmd:
            self.extern_cmd_textCtrl.SetValue(self.ext_scan_cmd)

    def readOptions(self):
        """
        Считать с контролов параметры сканирования.
        """
        self.scanner = self.scanner_comboBox.GetStringSelection()
        self.scan_source = scan_manager.SCAN_SOURCES[self.source_comboBox.GetCurrentSelection()]
        self.scan_mode = scan_manager.SCAN_MODES[self.mode_comboBox.GetCurrentSelection()]
        self.is_multi_scan = self.multiscan_checkBox.IsChecked()
        self.is_preview = self.preview_checkBox.IsChecked()
        self.page_size = scan_manager.SCAN_PAGE_SIZES[self.pagesize_comboBox.GetCurrentSelection()]
        self.scan_area = (self.left_spinCtrl.GetValue(),
                          self.top_spinCtrl.GetValue(),
                          self.right_spinCtrl.GetValue(),
                          self.bottom_spinCtrl.GetValue())
        self.scan_dir = self.scan_dirPicker.GetPath()
        self.scan_filename = self.filename_textCtrl.GetValue()
        self.scan_filetype = scan_manager.SCAN_FILE_TYPES[self.fileext_comboBox.GetCurrentSelection()]
        self.depth = self.depth_spinCtrl.GetValue()
        self.ext_scan_cmd = self.extern_cmd_textCtrl.GetValue()

    def setOptions(self, **options):
        """
        Установить опции сканирования в диалоговом окне.
        @param options: Опции.
        @return: True/False.
        """
        for option_name, option_value in options.items():
            if hasattr(self, option_name):
                try:
                    setattr(self, option_name, option_value)
                    log.info(u'Установлена опция <%s>. Значение <%s>' % (option_name, option_value))
                except:
                    log.warning(u'Ошибка установки опции <%s>. Значние <%s>' % (option_name, option_value))
        # После установки атрибутов отобразить их в диалоговом окне
        self.showOptions()

    def onCanceButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Отмена>.
        """
        self.EndModal(wx.CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Сканировать>.
        """
        self.readOptions()
        self.runScan()

        # Сохранить те параметры которые выбрали
        self.saveOptions()

        self.EndModal(wx.OK)
        event.Skip()

    def onExternButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Инструмент сканирования...>.
        """
        self.readOptions()
        self.runExtScan()

        # Сохранить те параметры которые выбрали
        self.saveOptions()

        self.EndModal(wx.OK)
        event.Skip()

    def initComboBoxScanners(self, sSelectScanner=None):
        """
        Инициализация комбобокса списка сканеров системы.
        @param sSelectScanner: Какой сканер выбрать после
            инициализации комбобокса,
            если None то выбирается первый в списке.
        """
        scanner_devices = self.scan_manager.getDeviceNames()

        self.scanner_comboBox.Clear()

        if scanner_devices:
            default_select = 0
            i = 0
            for scanner_name in scanner_devices:

                img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'scanner.png'))
                if scanner_name == sSelectScanner:
                    default_select = i

                self.scanner_comboBox.Append(scanner_name, wx.Image.ConvertToBitmap(wx.Image(img_filename)))
                i += 1

            self.scanner_comboBox.Select(default_select)
        else:
            log.warning(u'Не найдены устройства сканирования')
            msg = u'Не найдены устройства сканирования. Проверте включены ли устройства/есть ли с ними соединение.'
            dlg.getWarningBox(u'ВНИМАНИЕ', msg)
            try:
                self.EndModal(wx.ID_CANCEL)
            except:
                log.fatal()

    def onMultiScanCheckBox(self, event):
        """
        Обработчик отметки параметра многостраничного сканирования.
            Если включается многостраничное сканирование, то
            файл сканирования может быть только PDF.
        """
        if event.IsChecked():
            self.fileext_comboBox.Select(0)
        event.Skip()

    def onFileTypeCombobox(self, event):
        """
        Обработчик выбора типа файла сканирования.
            Если выбирается тип файла сканирования
            не PDF/формат картинки, то отключается
            многостраничное сканирование.
        """
        if event.GetSelection():
            self.multiscan_checkBox.SetValue(False)
        event.Skip()


def do_scan_dlg(parent=None, options=None, title=None):
    """
    Вызов диалоговой формы сканирования.
    @param parent: Родительское окно.
    @param options: Параметры сканирования.
    @param title: Заголовок окна.
    @return: True/False.
    """
    result = True
    scan_dlg = icScannerDlg(parent=parent)
    if title:
        scan_dlg.SetTitle(title)
        
    if options:
        scan_dlg.setOptions(**options)

    if scan_dlg.scan_manager.isDevices():
        dlg_result = scan_dlg.ShowModal()
        result = dlg_result == wx.ID_OK
    else:
        msg = u'Не найдены устройства сканирования. Проверте включены ли устройства/есть ли с ними соединение.'
        dlg.getWarningBox(u'ВНИМАНИЕ', msg)
        result = False

    # ВНИМАНИЕ! Необходимо удалять диалоговое окно
    # после использования иначе не происходит
    # закрытие программы
    scan_dlg.Destroy()

    return result
