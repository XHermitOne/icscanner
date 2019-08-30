#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер управления сканированием.

Используемые библиотеки:

python-sane - Библиотека управления сканером.
В Ubuntu 16.04 присутствует версия 2.8.2.
Установка:
************************************
sudo apt-get install python-sane
************************************

reportlab - Библиотека генерации PDF файлов.
Используется для сканирования сразу
нескольких листов в один документ.
Установка:
***************************************
sudo apt-get install python-reportlab
***************************************
"""

import traceback
import os
import os.path
import sane
import wx
from reportlab.pdfgen import canvas

from ic.std.log import log
from ic.std.utils import filefunc
from ic import config

from . import ext_scan_dlg

__version__ = (1, 1, 1, 1)

# Режимы сканирования
GREY_SCAN_MODE = 'Grey'
COLOR_SCAN_MODE = 'Color'
LINEART_SCAN_MODE = 'Lineart'
HALFTONE_SCAN_MODE = 'Halftone'
SCAN_MODES = (LINEART_SCAN_MODE, HALFTONE_SCAN_MODE,
              GREY_SCAN_MODE, COLOR_SCAN_MODE)

# Имя файла скана PDF по умолчанию при многостраничном сканировании
DEFAULT_PDF_SCAN_FILENAME = os.path.join(filefunc.getHomePath(),
                                         config.PROFILE_DIRNAME,
                                         'scan.pdf')

# Источники
FLATBED_SOURCE = 'Flatbed'
FRONT_SOURCE = 'ADF Front'
BACK_SOURCE = 'ADF Back'
DUPLEX_SOURCE = 'ADF Duplex'
SCAN_SOURCES = (FLATBED_SOURCE, FRONT_SOURCE, BACK_SOURCE, DUPLEX_SOURCE)

# Размеры страниц
A4_PORTRAIT_PAGE_SIZE = (210.0, 297.0)
A4_LANDSCAPE_PAGE_SIZE = (297.0, 210.0)
A3_PORTRAIT_PAGE_SIZE = (297.0, 420.0)
A3_LANDSCAPE_PAGE_SIZE = (420.0, 297.0)
SCAN_PAGE_SIZES = (A4_PORTRAIT_PAGE_SIZE, A3_PORTRAIT_PAGE_SIZE)

# Поддерживаемые типы файлов сканов
PDF_FILE_TYPE = 'pdf'
JPEG_FILE_TYPE = 'jpeg'
JPG_FILE_TYPE = 'jpg'
TIF_FILE_TYPE = 'tif'
BMP_FILE_TYPE = 'bmp'
SCAN_FILE_TYPES = (PDF_FILE_TYPE, JPEG_FILE_TYPE, JPG_FILE_TYPE,
                   TIF_FILE_TYPE, BMP_FILE_TYPE)

# Глубина по умолчанию
DEFAULT_DEPTH = 8

MULTISCAN_PAGE_FILENAME = os.path.join(filefunc.getHomePath(),
                                       config.PROFILE_DIRNAME,
                                       'page%d.jpg')

# Порядок установки опций сканирования
# ВНИМАНИЕ! Этот порядок важен т.к. опции
# взаимно контролирующиеся
SCAN_OPTIONS_ORDER = ('source', 'mode', 'depth',
                      'page_width', 'page_height',
                      'tl_x', 'tl_y', 'br_x', 'br_y')


# Размер сканированной страницы в точках по умолчанию
# Значения определены экспериментальным путем
DEFAULT_IMAGE_PAGE_SIZE = (4961, 7016)

# Сообщение об ошибке при застревании документа в лотке подачи
DOC_FEEDER_JAMMED_ERR = 'error: Document feeder jammed'


class icScanManager(object):
    """
    Менеджер управления сканированием.
    """
    def init(self):
        """
        Инициализация.
        """
        self.sane_ver = sane.init()
        self.devices = sane.get_devices()

        # Задублированные опции сканирования
        self.options = dict()

    def init_options_order(self):
        """
        Порядок установки опций сканирования. Инициализация.
        ВНИМАНИЕ! Этот порядок важен т.к. опции
        взаимно контролирующиеся
        @return: True/False
        """
        options = self.getScanOptions()
        if options is None:
            return False

        global SCAN_OPTIONS_ORDER
        SCAN_OPTIONS_ORDER = tuple([option[1].replace('-', '_') for option in options])
        return True

    def getSaneVersion(self):
        """
        Версия пакета Sane.
        Определяется после нициализации.
        @return: Версия пакета Sane.
        """
        if hasattr(self, 'sane_ver'):
            return self.sane_ver
        return None

    def getDeviceNames(self):
        """
        Список имен доступных сканеров.
        @return: Список имен доступных сканеров.
        """
        if hasattr(self, 'devices'):
            return tuple([device[0] for device in self.devices])
        return tuple()

    def isDevices(self):
        """
        Доступны сканеры?
        @return: True/False.
        """
        if hasattr(self, 'devices'):
            return bool(self.devices)
        return False

    def open(self, device_name):
        """
        Открыть устройство сканирования.
        @param device_name: Имя устройства сканирования.
        @return: Объект устройства сканирования.
        """
        try:
            self.scan_device_obj = sane.open(device_name)
            self.init_options_order()
        except:
            log.fatal(u'Ошибка открытия устройства сканирования <%s>' % device_name)
            self.scan_device_obj = None
        return self.scan_device_obj

    def close(self):
        """
        Закрыть устройство сканирования.
        @return: True/False
        """
        try:
            self.scan_device_obj.close()
            self.scan_device_obj = None
            return True
        except AttributeError:
            log.fatal(u'Устройство сканирования не открыто')

        return False

    def getScanOptions(self):
        """
        Опции сканирования.
        @return: Опции сканирования.
        """
        try:
            return self.scan_device_obj.get_options()
        except AttributeError:
            log.fatal(u'Устройство сканирования не открыто')
            return None

    def getScanOptionsDict(self):
        """
        Опции сканирования в виде словаря.
        @return: Опции сканирования в виде словаря.
        """
        options = self.getScanOptions()
        if options:
            return dict([(option[1], option) for option in options])
        return dict()

    def setScanOptions(self, **options):
        """
        Установить опции сканирования
        @param options: Значения опций.
        @return: True - все прошло удачно / False - ошибка.
        """
        try:
            global SCAN_OPTIONS_ORDER
            for option_name in SCAN_OPTIONS_ORDER:
                if option_name in options:
                    option_val = options[option_name]
                    try:
                        setattr(self.scan_device_obj, option_name, option_val)
                        log.info(u'Установка опции сканирования <%s>. Значение <%s>' % (option_name, option_val))
                        # Запомнить выставленные значения опций
                        # Может быть так что устанавливаем опции в устройстве
                        # а они по не понятной причине не выставляются:-(
                        self.options[option_name] = option_val
                    except:
                        log.warning(u'Ошибка установки опции сканирования <%s>. Значение <%s>' % (option_name, option_val))
            return True
        except:
            log.fatal(u'Ошибка установки опций сканирования')
        return False

    def getScanParameters(self):
        """
        Параметры сканирования.
        @return: Параметры сканирования.
        """
        try:
            return self.scan_device_obj.get_parameters()
        except AttributeError:
            log.fatal(u'Устройство сканирования не открыто')
            return None

    def getMaxSheets(self):
        """
        Максимальное количество листов, помещаемых в лоток сканера.
        @return: Максимальное количество листов, помещаемых в лоток сканера.
        """
        return config.get_glob_var('DEFAULT_SCANNER_MAX_SHEETS')

    def isDuplexOption(self):
        """
        Проверка включена ли опция дуплекса.
        @return: True/False.
        """
        options = self.options
        if options:
            try:
                if 'source' in options:
                    # Проверка по выставленным опциям
                    scan_source_opt = options['source']
                else:
                    # Проверка по опциям устройства
                    dev_options = self.getScanOptionsDict()
                    scan_source = dev_options['source']
                    scan_source_opt = scan_source[8][scan_source[4]]
                return 'Duplex' in scan_source_opt
            except:
                log.fatal(u'Ошибка определения вкл. опции сканирования дуплекс')
        else:
            log.warning(u'Не определены опции сканирования. Дуплекс отключен по умолчанию')
        return False

    def setDuplexOption(self, is_duplex=False):
        """
        Вкл./Выкл. опцию дуплекса.
        @param is_duplex: Признак 2-стороннего сканирования.
        """
        src = DUPLEX_SOURCE if is_duplex else FRONT_SOURCE
        return self.setScanOptions(source=src)

    def startScan(self):
        """
        Запуск сканирования.
        @return: True/False.
        """
        try:
            self.scan_device_obj.start()
            return True
        except:
            log.fatal(u'Ошибка запуска сканирования')
        return False

    def scan(self, scan_filename=None):
        """
        Сканировать документ и сохранить его в файл.
        @param scan_filename: Имя файла скана.
            Если имя файла не указано, то происходит сканирование и
            возвращается объект PIL.Image.
        @return: Имя файла скана или объект PIL.Image.
            None - в случае ошибки.
        """
        try:
            image = self.scan_device_obj.snap()

            if scan_filename:
                # Сохранить в указанный файл
                image.save(scan_filename)
                return scan_filename
            # Не сохраняем в файл. Нам нужен объект образа сканирования.
            return image
        except:
            log.fatal(u'Ошибка сканирования')

            # Так отображаем ошибки сканирования
            trace_txt = traceback.format_exc()
            if DOC_FEEDER_JAMMED_ERR in trace_txt:
                self.show_scan_error_msg(u'Застревание документа в лотке подачи бумаги')

        return None

    def scanSingle(self, scan_filename=None):
        """
        Одностраничное сканирование
        Если вкл. ДУПЛЕКС и выключено многостраничное сканирование,
        то надо отсканировать 1 лист с 2-х сторон.
        @param scan_filename: Имя файла скана.
            Если имя файла не указано, то происходит сканирование и
            возвращается объект PIL.Image.
        @return: True - все прошло успешно. False - ошибка.
        """
        if self.isDuplexOption():
            # Если вкл. ДУПЛЕКС и выключено многостраничное сканирование,
            # то надо отсканировать 1 лист с 2-х сторон
            log.debug(u'Сканирование дуплекс')
            return self.scanMulti(scan_filename, 2)
        # Сканирование одной страницы
        log.debug(u'Одностороннее сканирование')
        self.startScan()
        scan_obj = self.scan(scan_filename)
        return scan_obj is not None

    def _imageDrawCanvas(self, image, canvas, n, page_size=DEFAULT_IMAGE_PAGE_SIZE):
        """
        Вывести отсканированую страницу на PDF холст.
        @param image: Объект образа отсканированной страницы.
        @param canvas: Объект PDF холста.
        @param n: Номер страницы.
        @param page_size: Размер страницы в точках,
            к которому будут приводиться все отсканированные страницы.
        @return: True/False.
        """
        if image:
            img_filename = os.path.join(filefunc.getHomePath(),
                                        MULTISCAN_PAGE_FILENAME % n)
            width, height = page_size
            image = image.resize((int(width), int(height)))
            image.save(img_filename)
            canvas.drawImage(img_filename, 0, 0)
            canvas.showPage()
            return True
        else:
            log.warning(u'Ошибка записи сканированой страницы [%d] в PDF файл' % n)
        return False

    def scanMulti(self, scan_filename=None, n_page=-1):
        """
        Многостраничное сканирование.
        @param scan_filename: Имя файла скана.
            Многостраничное сканирование производится в PDF файл.
            В функции происходит проверка на расширение имени файла.
            Если имя файла не указано, то берется имя файла по умолчанию.
            ~/.icscanner/scan.pdf
        @param n_page: Количество сканируемых страниц.
            Если -1, то сканируются все возможные страницы.
        @return: True - все прошло успешно. False - ошибка.
        """
        if scan_filename is None:
            scan_filename = DEFAULT_PDF_SCAN_FILENAME

        file_ext = os.path.splitext(scan_filename)[1]
        if file_ext.lower() != '.pdf':
            log.warning(u'Не корректный тип файла для сохранения результата многостраничного сканирования')
            return False

        try:
            scan = self.scan_device_obj.multi_scan()

            scan_canvas = canvas.Canvas(scan_filename, pagesize=DEFAULT_IMAGE_PAGE_SIZE)

            if n_page < 0:
                # Сканирование всех возможных страниц
                is_stop_scan = False
                i_page = 0
                while not is_stop_scan:
                    image = None
                    try:
                        image = scan.next()
                    except StopIteration:
                        is_stop_scan = True
                        continue

                    result = self._imageDrawCanvas(image, scan_canvas, i_page)
                    if not result:
                        continue

                    i_page += 1
            else:
                # Сканирование определенное кол-во страниц
                for i_page in range(n_page):
                    image = None
                    try:
                        image = scan.next()
                    except StopIteration:
                        continue
                    result = self._imageDrawCanvas(image, scan_canvas, i_page)
                    if not result:
                        continue
            # Сохранить PDF холст
            scan_canvas.save()
            return True
        except:
            log.fatal(u'Ошибка многостраничного сканирования')

            # Так отображаем ошибки сканирования
            trace_txt = traceback.format_exc()
            if DOC_FEEDER_JAMMED_ERR in trace_txt:
                self.show_scan_error_msg(u'Застревание документа в лотке подачи бумаги')

        return False

    def show_scan_error_msg(self, err_msg=u''):
        """
        Функция отображения ошибок сканирования.
        @param err_msg: Сообщение об ошибке.
        """
        log.error(u'ОШИБКА СКАНИРОВАНИЯ. %s' % err_msg)

        try:
            import wx
            from ic.std.dlg import dlgfunc

            app = wx.GetApp()
            if not app:
                app = wx.PySimpleApp()
                dlgfunc.getErrBox(u'ОШИБКА СКАНИРОВАНИЯ', err_msg, parent=None)
                app.MainLoop()
            else:
                dlgfunc.getErrBox(u'ОШИБКА СКАНИРОВАНИЯ', err_msg, parent=app.GetTopWindow())
        except:
            # Если не отобразим сообщение об ошибке, то процесс
            # сканирования не должен остановиться
            log.fatal(u'Ошибка в функиции <show_scan_error_msg> менеджера сканирования')

    def scan_pack(self, scan_filenames=()):
        """
        Сканировать документы в пакетном режиме и сохранить их в файлы.        
        @param scan_filenames: Имена файлов скана с указанием количества листов
            и признаком 2-стороннего сканирования.
            Например:
                ('D:/tmp/scan001', 3, True), ('D:/tmp/scan002', 1, False), ('D:/tmp/scn003', 2, True), ...
        @return: Список имен файлов скана. None - в случае ошибки.
        """
        result = list()
        # Счетчик отсканированных листов
        tray_sheet_count = 0
        # Объем лотка в листах
        max_sheets = self.getMaxSheets()

        # В пакетном режиме не используем диалоговое окно
        # Но в случае режима склеивания документа по частям диалоговые окна используются
        # Объект приложения для управления диалоговыми окнами
        wx_app = None

        for scan_filename, n_pages, is_duplex in scan_filenames:
            tray_sheet_count += n_pages if not is_duplex else n_pages/2

            if tray_sheet_count <= max_sheets:
                # Пока счетчик сканирования не превысил ограничение объема лотка,
                # то продолжаем обычное сканирование
                scan_result = self.scan_pack_part(scan_filename, n_pages, is_duplex)
                result.append(scan_filename if scan_result and os.path.exists(scan_filename) else None)
            else:
                log.debug(u'Включение режима сканирования документа <%s> по частям. Количество страниц [%d] Текущий счетчик %d. ' % (scan_filename, n_pages, tray_sheet_count))
                if wx_app is None:
                    # Внимание! Приложение создается для
                    # управления диалоговыми окнами
                    wx_app = wx.PySimpleApp()
                    # ВНИМАНИЕ! Выставить русскую локаль
                    # Это необходимо для корректного отображения календарей,
                    # форматов дат, времени, данных и т.п.
                    locale = wx.Locale()
                    locale.Init(wx.LANGUAGE_RUSSIAN)

                # Если в лотке кончилась бумага, то надо запустить процедуру склейки последнего
                # документа
                glue_result = self.scan_glue(scan_filename, n_pages, is_duplex)
                # М.б. нажата <Отмена> или какая то ошибка
                result.append(scan_filename if glue_result and os.path.exists(scan_filename) else None)

                # ВНИМАНИЕ! После успешно отсканированного большого документа
                # сбрасываем счетчик отсканированных листов
                tray_sheet_count = 0

        # ВНИМАНИЕ! Т.к. взаимодействие построено на модальных диалоговых
        # окнах, то MainLoop делать не надо иначе основное приложение зависает
        # if wx_app:
        #    wx_app.MainLoop()

        return result

    def scan_pack_part(self, scan_filename, n_pages, is_duplex):
        """
        Сканирование одной части пакета.
        @param scan_filename: Имя результирующего файла скана.
        @param n_pages: Количество листов.
        @param is_duplex: Двустороннее сканирование?
        @return: True/False.
        """
        # Вкл./Выкл. 2-стороннее сканирование
        self.setDuplexOption(is_duplex)
        if n_pages == 1:
            scan_result = self.scanSingle(scan_filename)
            return scan_result
        elif n_pages > 1:
            scan_result = self.scanMulti(scan_filename, n_pages)
            return scan_result
        else:
            log.warning(u'Не корректное количество страниц <%s> в пакетном режиме сканирования' % n_pages)
        return False

    def scan_glue(self, scan_filename, n_pages, is_duplex):
        """
        Запуск режима склеивания документа из частей.
        @param scan_filename: Имя результирующего файла скана.
        @param n_pages: Количество страниц.
        @param is_duplex: Двустороннее сканирование?
        @return: True/False.
        """
        # Вкл./Выкл. 2-стороннее сканирование
        self.setDuplexOption(is_duplex)
        n_sheets = n_pages/2 if is_duplex else n_pages
        return ext_scan_dlg.scan_glue_mode(self, scan_filename, n_sheets, is_duplex,
                                           self.getMaxSheets())


def test():
    """
    Функция тестирования.
    """
    scan_manager = icScanManager()
    scan_manager.init()
    devices = scan_manager.getDeviceNames()
    print(devices)

    scan_manager.open(devices[0])
    scan_manager.startScan()
    scan_manager.scan()
    scan_manager.close()

    scan_manager.open(devices[0])
    scan_manager.startScan()
    scan_manager.scanMulti('test.pdf')
    scan_manager.close()


if __name__ == '__main__':
    test()
