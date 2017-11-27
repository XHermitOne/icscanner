#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
icScanner - Программа запуска сканирования документов.
            Пакетной обработки сканированных документов.

Параметры коммандной строки:
    
    python icscanner.py <Параметры запуска>
    
Параметры запуска:

    [Помощь и отладка]
        --help|-h|-?        Напечатать строки помощи
        --version|-v        Напечатать версию программы
        --debug|-d          Режим отладки
        --log|-l            Режим журналирования

   [Режимы запуска]
        --scanner=          Явное указание имени сканера
        --source=           Источник сканирования:
                            Flatbed     (Планшетный)
                            ADF_Front   (Фронтальная сторона)
                            ADF_Back    (Обратная сторона)
                            ADF_Duplex  (Дуплекс/Обе стороны)
        --mode=             Режим сканирования:
                            Lineart     (Штриховой)
                            Halftone    (Полутоновой)
                            Grey        (Черно-белый)
                            Color       (Цветной)
        --depth=            Глубина. По умолчанию 8
        --multi_scan        Вкл. режим многостраничного сканирования
        --preview           Вкл. просмотр результата сканирования
        --page_size=        Размер страницы:
                            A4 или A3
        --area=             Область сканирования
        --scan_dir=         Папка сканирования
        --file_name=        Имя файла сканирования (без расширения)
                            В случае пакетной обработки, необходимо
                            указать имена файлов через <;>
        --file_type=        Тип файла сканирования:
                            PDF, JPEG, JPG, TIF, BMP
        --ext_cmd=          Команда запуска внешнего
                            инструмента сканирования
        --pack_mode         Включение режима пакетной обработки.
                            Пакетный режим подразумевает запуск программы
                            без диалогового окна.
        --pack_pages=       Количество страниц в каждом документе
                            Если --pack_pages не указан, то считаем, 
                            что все документы одностраничные.
                            В указании страниц можно указать через /
                            есть 2-х стороннее сканирование или нет.
                            Например: 2/1 - 2 листа с двух сторон
                            3/0 - 3 листа с одной стороны
        --max_sheets=       Ограничение количества листов в лотке сканнера
"""

import sys
import getopt
import wx

from ic import config
from ic.std.log import log
from scanner import scanner_dlg
from scanner import scan_manager


__version__ = (0, 2, 1, 1)


def main(argv):
    """
    Основная запускающая функция.
    @param argv: Список параметров коммандной строки.
    """
    # Разбираем аргументы командной строки
    try:
        options, args = getopt.getopt(argv, 'h?vdl',
                                      ['help', 'version', 'debug', 'log',
                                       'scanner=', 'source=',
                                       'mode=', 'multi_scan', 'preview',
                                       'page_size=', 'area=',
                                       'scan_dir=',
                                       'file_name=', 'file_type=',
                                       'ext_cmd=',
                                       'pack_mode', 'pack_pages=',
                                       'glue', 'max_sheets='])
    except getopt.error, msg:
        print(msg)
        print('For help use --help option')
        sys.exit(2)

    # Инициализоция системы журналирования
    log.init(config)

    txt_version = '.'.join([str(ver) for ver in __version__])
    cmd_options = dict()
    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            print(__doc__)
            sys.exit(0)   
        elif option in ('-v', '--version'):
            print('icScanner version: %s' % txt_version)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            config.set_glob_var('DEBUG_MODE', True)
        elif option in ('-l', '--log'):
            config.set_glob_var('LOG_MODE', True)
        elif option in ('--scanner', ):
            cmd_options['scanner'] = arg
        elif option in ('--source',):
            cmd_options['scan_source'] = arg
        elif option in ('--mode',):
            cmd_options['scan_mode'] = arg
        elif option in ('--multi_scan',):
            cmd_options['is_multi_scan'] = True
        elif option in ('--preview',):
            cmd_options['is_preview'] = True
        elif option in ('--page_size',):
            if arg in ('A4', 'a4'):
                cmd_options['page_size'] = scan_manager.A4_PORTRAIT_PAGE_SIZE
            elif arg in ('A3', 'a3'):
                cmd_options['page_size'] = scan_manager.A3_PORTRAIT_PAGE_SIZE
            else:
                log.warning(u'Не обрабатываемый размер страницы <%s>' % arg)
        elif option in ('--area',):
            try:
                area = tuple([float(x.strip()) for x in arg.split(',')])
                cmd_options['scan_area'] = area
            except:
                log.fatal(u'Ошибка парсинга параметра области сканирования <%s>' % arg)
        elif option in ('--scan_dir',):
            cmd_options['scan_dir'] = arg
        elif option in ('--file_name',):
            cmd_options['scan_filename'] = arg
        elif option in ('--file_type',):
            cmd_options['scan_filetype'] = arg.lower()
        elif option in ('--depth',):
            cmd_options['depth'] = int(arg)
        elif option in ('--ext_cmd',):
            cmd_options['ext_scan_cmd'] = arg
        elif option in ('--pack_mode',):
            cmd_options['pack_mode'] = True
        elif option in ('--pack_pages',):
            cmd_options['pack_pages'] = arg
        elif option in ('--max_sheets',):
            config.set_glob_var('DEFAULT_SCANNER_MAX_SHEETS', int(arg))
        else:
            log.warning(u'Не обрабатываемый параметр коммандной строки <%s>' % option)

    # По умолчанию пакетный режим отключен+
    #                                     v
    if not cmd_options.get('pack_mode', False):
        # Внимание! Приложение создается для
        # управления диалоговыми окнами
        app = wx.PySimpleApp()
        # ВНИМАНИЕ! Выставить русскую локаль
        # Это необходимо для корректного отображения календарей,
        # форматов дат, времени, данных и т.п.
        locale = wx.Locale()
        locale.Init(wx.LANGUAGE_RUSSIAN)

        scanner_dlg.do_scan_dlg(options=cmd_options, 
                                title=u'Сканирование. icScanner ' + txt_version)
        app.MainLoop()
    else:
        # В пакетном режиме не используем диалоговое окно
        # Но в случае режима склеивания документа по частям диалоговые окна используются
        filenames = cmd_options.get('scan_filename', u'').split(';')
        pack_page_list = cmd_options.get('pack_pages', u'').split(';')
        n_pages = [int(pack_page.split('/')[0]) if '/' in pack_page else int(pack_page) for pack_page in pack_page_list]
        duplexes = [bool(int(pack_page.split('/')[1])) if '/' in pack_page else False for pack_page in pack_page_list]
        scan_filenames = [(filename, n_pages[i] if i < len(n_pages) else 1,
                           duplexes[i] if i < len(duplexes) else False) for i, filename in enumerate(filenames)]
        scan_admin = scanner_dlg.icScanAdministrator()
        # Установить дополнительные опции из коммандной строки
        scan_admin.setExtOptions(scan_dir=cmd_options['scan_dir'])
        scan_admin.runScanPack(*scan_filenames)


if __name__ == '__main__':
    main(sys.argv[1:])
