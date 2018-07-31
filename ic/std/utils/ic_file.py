#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами.
"""

# --- Подключение пакетов ---
import wx
import os
import os.path
import shutil   # Для реализации высокоуровневых функций работы с файлами
import sys
import time
import glob     # Для поиска файлов по маске/шаблону
import platform

from ..log import log
from ..dlg import dlg

import ic.config

__version__ = (1, 1, 1, 1)

_ = wx.GetTranslation


# --- Функции пользователя ---
def GetMakeFileTime(FileName_):
    """
    Время создания файла. Если файла не существует то 0.
    """
    if os.path.exists(FileName_):
        return os.path.getmtime(FileName_)
    return 0


def MakeDirs(Path_):
    """
    Создает каталоги и не ругается.
    """
    try:
        return os.makedirs(Path_)
    except:
        log.fatal(u'Ошибка создания каталога <%s>' % Path_)


def icChangeExt(FileName_, NewExt_):
    """
    Поменять у файла расширение.
    @param FileName_: Полное имя файла.
    @param NewExt_: Новое расширение файла (Например: '.bak').
    @return: Возвращает новое полное имя файла.
    """
    try:
        new_name = os.path.splitext(FileName_)[0]+NewExt_
        if os.path.isfile(new_name):
            os.remove(new_name)     # если файл существует, то удалить
        if os.path.exists(FileName_):
            os.rename(FileName_, new_name)
            return new_name
    except:
        log.fatal(u'Ошибка изменения расширения файла <%s> -> <%s>' % (FileName_, NewExt_))
    return None


def icCopyFile(FileName_, NewFileName_, Rewrite_=True):
    """
    Создает копию файла с новым именем.
    @param FileName_: Полное имя файла.
    @param NewFileName_: Новое имя файла.
    @param Rewrite_: True-если новый файл уже существует, 
        то переписать его молча. False-если новый файл уже существует, 
        то выдать сообщение о подтверждении перезаписи файла.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        # --- Проверка существования файла-источника ---
        if not os.path.isfile(FileName_):
            dlg.getWarningBox(u'ОШИБКА', u'Файл <%s> не существует.' % FileName_)
            return False
        # --- Проверка перезаписи уже существуещего файла ---
        # Выводить сообщение что файл уже существует?
        if not Rewrite_:
            # Файл уже существует?
            if os.path.isfile(NewFileName_):
                if dlg.getAskBox(u'КОПИРВАНИЕ',
                                 u'Файл <%s> уже существует. Переписать?' % NewFileName_) == wx.NO:
                    return False

        # --- Реализация копирования файла ---
        MakeDirs(os.path.dirname(NewFileName_))
        if os.path.exists(FileName_) and os.path.exists(NewFileName_) and os.path.samefile(FileName_, NewFileName_):
            log.warning(u'Попытка скопировать файл <%s> самого в себя' % FileName_)
        else:
            shutil.copyfile(FileName_, NewFileName_)
        return True
    except:
        log.fatal(u'Ошибка копирования файла <%s> -> <%s>' % (FileName_, NewFileName_))
        return False


def icCreateBAKFile(FileName_, BAKFileExt_='.bak'):
    """
    Создает копию файла с новым расширением BAK.
    @param FileName_: Полное имя файла.
    @param BAKFileExt_: Расширение BAK файла.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        if not os.path.exists(FileName_):
            log.warning(u'Не найден файл <%s> для создания его резервной копии' % FileName_)
            return False

        bak_name = os.path.splitext(FileName_)[0]+BAKFileExt_
        return icCopyFile(FileName_, bak_name)
    except:
        log.fatal(u'Ошибка создания BAK файла <%s>' % FileName_)
        return False


def GetSubDirs(Path_):
    """
    Функция возвращает список поддиректорий.
    @param Path_: Дирикторий.
    @return: В случае ошибки возвращает None.
    """
    try:
        if not os.path.exists(Path_):
            log.warning(u'Путь <%s> не найден для определения списка поддриекторий' % Path_)
            return list()
        dir_list = [os.path.join(Path_, path) for path in os.listdir(Path_)]
        dir_list = [path for path in dir_list if os.path.isdir(path)]
        return dir_list
    except:
        log.fatal(u'Ошибка чтения списка поддиректорий <%s>' % Path_)
        return None


def GetSubDirsFilter(Path_, Filter_=('.svn','.SVN','.Svn')):
    """
    Функция возвращает список поддиректорий с отфильтрованными папками.
    @param Path_: Дирикторий.
    @param Filter_: Список недопустимых имен папок.
    @return: В случае ошибки возвращает None.
    """
    try:
        if not os.path.exists(Path_):
            log.warning(u'Не найден путь <%s> для определения списка поддиректорий' % Path_)
            return list()

        dir_list = [os.path.join(Path_, path) for path in os.listdir(Path_)]
        dir_list = [path for path in dir_list if os.path.isdir(path)]
        dir_list = [d for d in dir_list if _pathFilter(d, Filter_)]
        return dir_list
    except:
        log.fatal(u'Ошибка чтения списка поддиректорий <%s>' % Path_)
        return None


def GetSubDirsFilterSVN(Path_):
    """
    Функция возвращает список поддиректорий с отфильтрованными папками Subversion.
    @param Path_: Дирикторий.
    @param Filter_: Список недопустимых имен папок.
    @return: В случае ошибки возвращает None.
    """
    return GetSubDirsFilter(Path_)


def GetFiles(Path_):
    """
    Функция возвращает список файлов в директории.
    @param Path_: Дирикторий.
    @return: В случае ошибки возвращает None.
    """
    try:
        if not os.path.exists(Path_):
            log.warning(u'Не найден путь <%s> для определения списка файлов директории' % Path_)
            return list()

        file_list = None
        file_list = [os.path.join(Path_, x.lower()) for x in os.listdir(Path_)]
        file_list = [x for x in file_list if os.path.isfile(x)]
        return file_list
    except:
        log.fatal(u'Ошибка чтения списка файлов <%s>' % Path_)
        return None


def GetFilesByExt(Path_, Ext_):
    """
    Функция возвращает список всех файлов в директории с указанным расширением.
    @param Path_: Путь.
    @param Ext_: Расширение, например '.pro'.
    @return: В случае ошибки возвращает None.
    """
    try:
        Path_ = getCurDirPrj(Path_)
        if not os.path.exists(Path_):
            log.warning(u'Путь <%s> не найден для определения списка файлов директории по расширению' % Path_)
            return list()

        if Ext_[0] != '.':
            Ext_ = '.' + Ext_
        Ext_ = Ext_.lower()
            
        file_list = None
        file_list = [os.path.join(Path_, file_name) for file_name in os.listdir(Path_)]
        file_list = [file_name for file_name in file_list if os.path.isfile(file_name) and
                     (os.path.splitext(file_name)[1].lower() == Ext_)]
        return file_list
    except:
        log.fatal(u'Ошибка чтения списка файлов <ext=%s, path=%s, list=%s>' % (Ext_, Path_, file_list))
        return None


def icCleanFileExt(Path_, Ext_):
    """
    Функция УДАЛЯЕТ РЕКУРСИВНО В ПОДДИРЕКТОРИЯХ все файлы в директории с
    заданным расширением.
    @param Path_: Путь.
    @param Ext_: Расширение.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        ok = True
        dir_list = os.listdir(Path_)
        for cur_item in dir_list:
            cur_file = Path_+cur_item
            if os.path.isfile(cur_file) and os.path.splitext(cur_file)[1] == Ext_:
                os.remove(cur_file)
            elif os.path.isdir(cur_file):
                ok = ok and icCleanFileExt(cur_file, Ext_)
        return ok
    except:
        return False        


def getFileExt(FileName_):
    """
    Получить расширение файла с точкой.
    """
    return os.path.splitext(FileName_)[1]


def icRelativePath(Path_):
    """
    Относительный путь.
    @param Path_: Путь.
    """
    Path_ = Path_.replace('\\', '/')
    cur_dir = os.getcwd()
    return Path_.replace(cur_dir, './').strip()


def icAbsolutePath(Path_):
    """
    Абсолютный путь.
    @param Path_: Путь.
    """
    try:
        Path_ = os.path.abspath(Path_)
        Path_ = Path_.replace('\\', '/').lower().strip()
        return Path_
    except:
        log.fatal(u'Ошибка определения абсолютного пути <%s>' % Path_)
        return Path_


def RelativePath(Path_, CurDir_=None):
    """
    Относительный путь. Путь приводится к виду Unix.
    @param Path_: Путь.
    @param CurDir_: Текущий путь.
    """
    if CurDir_ is None:
        import ic.engine.ic_user
        CurDir_ = os.path.dirname(ic.engine.ic_user.icGet('PRJ_DIR')).replace('\\', '/').lower()
    if CurDir_:
        Path_ = Path_.replace('\\', '/').lower().strip()
        return Path_.replace(CurDir_, '.')
    return Path_


def getCurDirPrj(Path_=None):
    """
    Текущий путь. Определяется относительно PRJ_DIR.
    """
    # Нормализация текущего пути
    if Path_ is None:
        try:
            import ic.engine.ic_user
            prj_dir = ic.engine.ic_user.icGet('PRJ_DIR')
            if prj_dir:
                Path_ = os.path.dirname(prj_dir)
            else:
                Path_ = getProfilePath()
        except:
            log.fatal(u'Ошибка определения пути <%s>' % Path_)
            Path_ = os.getcwd()
    Path_ = Path_.replace('\\', '/')
    if Path_[-1] != '/':
        Path_ += '/'
    return Path_


def AbsolutePath(sPath, sCurDir=None):
    """ 
    Абсолютный путь. Путь приводится к виду Unix. 
    @param sPath: Путь.
    @param sCurDir: Текущий путь.
    """
    try:
        # Нормализация текущего пути
        sCurDir = getCurDirPrj(sCurDir)
        # Коррекция самого пути
        sPath = os.path.abspath(sPath.replace('./', sCurDir).strip())
        return sPath
    except:
        log.fatal(u'Ошибка определения абсолютног пути <%s>. Текущая директория <%s>' % (sPath, sCurDir))
        return sPath


def PathFile(Path_, File_):
    """
    Корректное представление общего имени файла.
    @param Path_: Путь.
    @param File_: Имя файла.
    """
    if not Path_:
        log.warning(u'Не определен путь для корректировки')
        return File_
    if not File_:
        log.warning(u'Не определено имя файла для корректировки')
        return File_

    Path_ = os.path.normpath(Path_)
    File_ = os.path.normpath(File_)
    relative_path = icRelativePath(Path_)
    # Этот путь уже присутствует в имени файла
    if File_.find(Path_) != -1 or File_.find(relative_path) != -1:
        return File_
    return os.path.join(relative_path, File_)


def NormPathWin(Path_):
    """
    Приведение пути к виду Windows.
    """
    if not Path_:
        return ''
        
    if Path_.find(' ') > -1 and Path_[0] != '\'' and Path_[-1] != '\'':
        return '\''+os.path.normpath(Path_).strip()+'\''
    else:
        return os.path.normpath(Path_).strip()


def NormPathUnix(Path_):
    """
    Приведение пути к виду UNIX.
    """
    return os.path.normpath(Path_).replace('\\', '/').strip()


def SamePathWin(Path1_, Path2_):
    """
    Проверка,  Path1_==Path2_.
    """
    return bool(NormPathWin(Path1_).lower() == NormPathWin(Path2_).lower())


def _pathFilter(Path_, Filter_):
    """
    Фильтрация путей.
    @return: Возвращает True если папок с указанными имена в фильтре нет в пути и
        False если наоборот.
    """
    path = os.path.normpath(Path_).replace('\\', '/')
    path_lst = path.split(os.path.sep)
    filter_result = True
    for cur_filter in Filter_:
        if cur_filter in path_lst:
            filter_result = False
            break
    return filter_result


def _addCopyDirWalk(args, CurDir_, CurNames_):
    """
    Функция рекурсивного обхода при добавлении папок и файлов в существующую.
    @param CurDir_: Текущая обрабатываемая папка.
    @param CurName_: Имена файлов и папок в текущей обрабатываемой папке.
    """
    from_dir = args[0]
    to_dir = args[1]
    not_copy_filter = args[2]
    
    if _pathFilter(CurDir_, not_copy_filter):
        paths = [os.path.join(CurDir_, name) for name in CurNames_ if name not in not_copy_filter]
        for path in paths:
            to_path = path.replace(from_dir, to_dir)
            if not os.path.exists(to_path):
                # Копировать если результирующего файла/папки не существует
                if os.path.isfile(path):
                    # Скопировать файл
                    icCopyFile(path, to_path)
                elif os.path.isdir(path):
                    # Создать директорию
                    try:
                        os.makedirs(to_path)
                    except:
                        log.fatal(u'Ошибка создания папки <%s>' % to_path)
                        raise


def addCopyDir(Dir_, ToDir_, NotCopyFilter_=('.svn', '.SVN', '.Svn')):
    """
    Дополнить папку ToDir_ файлами и папками из Dir_
    @param Dir_: Папка/директория,  которая копируется.
    @param ToDir_: Папка/директория, в которую копируется Dir_.
    @param NotCopyFilter_: Не копировать файлы/папки.
    """
    try:
        os.walk(Dir_, _addCopyDirWalk, (Dir_, ToDir_, NotCopyFilter_))
        return True
    except:
        log.fatal(u'Ошибка дополнения папки из <%s> в <%s>' % (Dir_, ToDir_))
        return False


def CopyDir(Dir_, ToDir_, ReWrite_=False, AddDir_=True):
    """
    Функция папку Dir_ в папку ToDir_ со всеми внутренними поддиректориями
    и файлами.
    @param Dir_: Папка/директория,  которая копируется.
    @param ToDir_: Папка/директория, в которую копируется Dir_.
    @param ReWrite_: Указание перезаписи директории,
        если она уже существует.
    @param AddDir_: Указание производить дополнение папки,
        в случае ко когда копируемые файлы/папки существуют.
    @return: Функция возвращает результат выполнения операции True/False.    
    """
    try:
        to_dir = os.path.join(ToDir_, os.path.basename(Dir_))
        if os.path.exists(to_dir) and ReWrite_:
            log.info(u'Удаление папки <%s>' % to_dir)
            shutil.rmtree(to_dir, 1)
        if os.path.exists(to_dir) and AddDir_:
            return addCopyDir(Dir_, to_dir)
        else:
            log.info(u'Копировние папки <%s> в <%s>' % (Dir_, to_dir))
            shutil.copytree(Dir_, to_dir)
        return True
    except:
        log.fatal(u'Ошибка копирования папки из <%s> в <%s>' % (Dir_, ToDir_))
        return False


def CloneDir(Dir_, NewDir_, ReWrite_=False):
    """
    Функция переносит все содержимое папки Dir_ в папку с новым именем NewDir_.
    @param Dir_: Папка/директория,  которая копируется.
    @param NewDir_: Новое имя папки/директории.
    @param ReWrite_: Указание перезаписи директории, если она
        уже существует.
    @return: Функция возвращает результат выполнения операции True/False.    
    """
    try:
        if os.path.exists(NewDir_) and ReWrite_:
            shutil.rmtree(NewDir_, 1)
        os.makedirs(NewDir_)
        for sub_dir in GetSubDirs(Dir_):
            shutil.copytree(sub_dir, NewDir_)
        for file_name in GetFiles(Dir_):
            icCopyFile(file_name, os.path.join(NewDir_, os.path.basename(file_name)))
        return True
    except:
        log.fatal(u'Ошибка клонирования папки из <%s> в <%s>' % (Dir_, NewDir_))
    return False


def IsSubDir(Dir1_, Dir2_):
    """
    Функция проверяет, является ли директория Dir1_ поддиректорией Dir2_.
    @return: Возвращает True/False.
    """
    dir1 = os.path.abspath(Dir1_)
    dir2 = os.path.abspath(Dir2_)
    if dir1 == dir2:
        return True
    else:
        sub_dirs = [path for path in [os.path.join(dir2, name) for name in os.listdir(dir2)] if os.path.isdir(path)]
        for cur_sub_dir in sub_dirs:
            find = IsSubDir(Dir1_, cur_sub_dir)
            if find:
                return find
    return False


def genDefaultBakFileName():
    """
    Генерация имени бак файла по текущему времени.
    """
    return time.strftime('_%d_%m_%Y_%H_%M_%S.bak', time.localtime(time.time()))


def getFilesByMask(FileMask_):
    """
    Список файлов по маске.
    @param FileMask_: Маска файлов. Например C:\Temp\*.dbf.
    @return: Возвращает список строк-полных путей к файлам.
        В случае ошибки None.
    """
    try:
        if isinstance(FileMask_, str):
            dir_path = os.path.dirname(FileMask_)
            if os.path.exists(dir_path):
                filenames = glob.glob(pathname=FileMask_, recursive=False)
                return [os.path.abspath(file_name) for file_name in filenames]
            else:
                log.warning(u'Не найден путь <%s> для определения списка файлов по маске <%s>' % (dir_path, FileMask_))
        elif isinstance(FileMask_, tuple) or isinstance(FileMask_, list):
            filenames = list()
            for file_mask in FileMask_:
                filenames = glob.glob(pathname=FileMask_, recursive=False)
                filenames += [os.path.abspath(file_name) for file_name in filenames]
            return filenames
        else:
            log.warning(u'Не поддерживаемый тип аргумента в функции getFilesByMask')
    except:
        log.fatal(u'Ошибка определения списка файлов по маске <%s>' % str(FileMask_))
    return []


def copyToDir(FileName_, DestDir_, Rewrite_=True):
    """
    Копировать файл в папку.
    @param FileName_: Имя файла.
    @param DestDir_: Папка в которую необходимо скопировать.
    @param Rewrite_: True-если новый файл уже существует, 
        то переписать его молча. False-если новый файл уже существует, 
        то выдать сообщение о подтверждении перезаписи файла.
    @return: Возвращает результат выполнения операции True/False.
    """
    return icCopyFile(FileName_, os.path.join(DestDir_,
                                              os.path.basename(FileName_)), Rewrite_)


def delAllFilesFilter(DelDir_, *Filter_):
    """
    Удаление всех файлов из папки с фильтрацией по маске файла. Удаление
    рекурсивное по поддиректориям.
    @param DelDir_: Папка-источник.
    @param Filter_: Список масок файлов которые нужно удалить.
        Например '*_pkl.tab'.
    """
    try:
        # Сначала обработка в поддиректориях
        subdirs = GetSubDirs(DelDir_)
        if subdirs:
            for sub_dir in subdirs:
                delAllFilesFilter(sub_dir, *Filter_)
        for file_mask in Filter_:
            del_files = getFilesByMask(os.path.join(DelDir_, file_mask))
            for del_file in del_files:
                os.remove(del_file)
                log.info(u'Удаление файла <%s>' % del_file)
        return True
    except:
        log.fatal(u'Ошибка удаления файлов %s из папки <%s>' % (str(Filter_), DelDir_))
        return None


def getPythonDir():
    """
    Папка в которую установлен Python.
    """
    return os.path.dirname(sys.executable)


def getPythonExe():
    """
    Полный путь к исполняемому интерпретатору Python.
    """
    return sys.executable


def getTempDir():
    """
    Временная директория
    """
    return os.environ['TMP']


def getTempFileName(Prefix_=None):
    """
    Генерируемое имя временного файла
    """
    return os.tempnam(getTempDir(), Prefix_)


def getHomePath():
    """
    Путь к домашней директории.
    @return: Строку-путь до папки пользователя.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'windows':
        home_path = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home_path = home_path.replace('\\', '/')
    elif os_platform == 'linux':
        home_path = os.environ['HOME']
    else:
        log.warning(u'Не поддерживаемая ОС <%s>' % os_platform)
        return None
    return os.path.normpath(home_path)


def getProfilePath(bAutoCreatePath=True):
    """
    Папка профиля программы DEFIS.
    @param bAutoCreatePath: Создать автоматически путь если его нет?
    @return: Путь до ~/.defis
    """
    home_path = getHomePath()
    if home_path:
        profile_path = os.path.join(home_path, ic.config.PROFILE_DIRNAME)
        if not os.path.exists(profile_path) and bAutoCreatePath:
            # Автоматическое создание пути
            try:
                os.makedirs(profile_path)
            except OSError:
                log.fatal(u'Ошибка создания пути профиля <%s>' % profile_path)
        return profile_path
    return '~/.defis'


def getPrjProfilePath(bAutoCreatePath=True):
    """
    Папка профиля прикладного проекта.
    @param bAutoCreatePath: Создать автоматически путь если его нет?
    @return: Путь до ~/.defis/имя_проекта/
    """
    profile_path = getProfilePath(bAutoCreatePath)

    prj_name = 'scanner'
    if prj_name:
        prj_profile_path = os.path.join(profile_path, prj_name)
    else:
        # Если в проект мы не вошли, то просто определяем папку профиля проекта
        # как папку профиля программы
        prj_profile_path = profile_path

    if not os.path.exists(prj_profile_path) and bAutoCreatePath:
        # Автоматическое создание пути
        try:
            os.makedirs(prj_profile_path)
        except OSError:
            log.fatal(u'Ошибка создания пути профиля проекта <%s>' % prj_profile_path)
    return prj_profile_path


def getProjectDir():
    """
    Папка проекта.
    @return: Папка проекта.
    """
    return ic_user.getPrjDir()


def getRootProjectDir():
    """
    Корневая папка проекта, в которой находяться все папки подсистем проекта.
    @return: Корневая папка проекта, в которой находяться все папки подсистем проекта.
    """
    prj_dir = getProjectDir()
    return os.path.dirname(prj_dir)

