#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций пользователя для работы с файлами.
"""

# --- Подключение пакетов ---
import os
import os.path
from ic.std.log import log

try:
    import shutil   # Для реализации высокоуровневых функций работы с файлами
    from shutil import rmtree as RemoveTreeDir
    from shutil import copytree as CopyTreeDir
except:
    log.error(u'Import Error shutil')

import sys

try:
    import time
except:
    log.error(u'Import Error time')

try:
    import glob     # Для поиска файлов по маске/шаблону
except:
    log.error(u'Import Error glob')


# --- Переопределение имен некоторых функций ---
from os import rename as Rename
from os import getcwd as GetCurDir
from os import remove as Remove
from os import unlink as UnLink
from os import listdir as ListDir

from os.path import isfile as IsFile
from os.path import isdir as IsDir
from os.path import split as Split
from os.path import splitext as SplitExt
from os.path import dirname as DirName
from os.path import basename as BaseName
from os.path import abspath as AbsPath
from os.path import walk as Walk
from os.path import join as Join
from os.path import exists as Exists
from os.path import normpath as NormPath
from os.path import getmtime as GetMakeFileTime
from os.path import getatime as GetAccessFileTime
from os.path import getsize as GetFileSize

from sys import path as PATH
from sys import argv as ARGV

try:
    import re
except:
    log.error(u'Import Error re')

try:
    from operator import truth
except:
    log.error(u'Import Error truth')

from . import ic_codecs
from . import util

try:
    import services.ic_std.ic_run.ic_user
except:
    log.error(u'Import Error in ic_std.ic_run.ic_user')

__version__ = (0, 0, 1, 3)


# --- Функции пользователя ---
def MakeDirs(Path_):
    """
    Создает каталоги и не ругается.
    """
    try:
        return os.makedirs(Path_)
    except:
        pass


def icChangeExt(FileName_,NewExt_):
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
        log.fatal(u'Ошибка изменения расширения файла %s на %s' % (FileName_, NewExt_))
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
            MsgBox(u'Файл %s не существует.' % FileName_,
                   u'Ошибка копирования файла.')
            return False

        # --- Проверка перезаписи уже существуещего файла ---
        # Выводить сообщение что файл уже существует?
        if not Rewrite_:
            MsgBox(u'Файл %s существует.' % NewFileName_,
                   u'Ошибка копирования файла.')
            return False

        # --- Реализация копирования файла ---
        MakeDirs(DirName(NewFileName_))
        shutil.copyfile(FileName_, NewFileName_)
        return True
    except:
        log.fatal(u'Ошибка копирования файла <%s> в <%s>' % (FileName_, NewFileName_))
        return False


def icCopyFilesByMask(fromMask, toMask, Rewrite_=True, bDelImage=False):
    """
    Копирует файлы по маске. Пример: "C:\WRK\p*.dbf" -> "Y:\WRK\pkt*.dbf"

    @type fromMask: C{string}
    @param fromMask: Маска, задающая файлы, которые надо копировать.
    @type toMask: C{string}
    @param toMask:Маска задает, куда надо копировать файлы.
    @type bDelImage: C{bool}
    @param bDelImage: Признак удаления образа файла. Если True - аналог переноса
    файлов с переименованием.
    """
    fileList = []

    fromMask = util.icUpper(fromMask.replace('\\', '/'))
    toMask = toMask.replace('\\', '/')
    dirName = '/'.join(fromMask.split('/')[:-1])
    #   Регулярное выражение для сравнения
    rm = re.compile(fromMask.replace('.', '\\.').replace('*', '.*').replace('$', '\\$'))
    ml1 = fromMask.split('*')
    ml2 = toMask.split('*')

    if os.path.isdir(dirName):
        #   Определяем список файлов
        dir_list = os.listdir(dirName)

        for indx, fl in enumerate(dir_list):
            path, fileName = os.path.split(fl)

            #   Определяем расширение файла
            try:
                ext = fileName.split('.')[1]
            except:
                ext = None

            fn = util.icUpper(dirName+'/'+fl)

            # Если очередное имя не является именем директории и удовлетворяет
            # шаблону, то соответствующий файл копируется в нужное место.
            if not os.path.isdir(fn) and truth(rm.match(fn)):
                #   Определяем новое имя файла
                copyName = fn
                for i, s in enumerate(ml2):
                    if i < len(ml1):
                        if ml1[i] and s:
                            copyName = copyName.replace(ml1[i], s)
                    else:
                        break

                log.info(u'Copy file %s -> %s' % (fn, copyName))
                if icCopyFile(fn, copyName, Rewrite_) and bDelImage:
                    Remove(fn)
                    log.info(u'Delete file <%s>' % fn)
    else:
        log.warning(u'Dir <%> didn\'t find' % dirName)


def icCreateBAKFile(FileName_, BAKFileExt_='.bak'):
    """
    Создает копию файла с новым расширением BAK.
    @param FileName_: Полное имя файла.
    @param BAKFileExt_: Расширение BAK файла.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        bak_name = os.path.splitext(FileName_)[0] + BAKFileExt_
        return icCopyFile(FileName_, bak_name)
    except:
        log.fatal(u'Ошибка создания BAK файла %s' % FileName_)
        return False


def GetSubDirs(Path_):
    """
    Функция возвращает список поддиректорий.
    @param Path_: Дирикторий.
    @return: В случае ошибки возвращает None.
    """
    try:
        dir_list = [Path_+'/'+path for path in ListDir(Path_)]
        dir_list = [path for path in dir_list if IsDir(path)]
        return dir_list
    except:
        log.fatal(u'Ошибка определения списка поддиректорий директории <%s>' % Path_)
        return None


def GetFiles(Path_):
    """
    Функция возвращает список файлов в директории.
    @param Path_: Дирикторий.
    @return: В случае ошибки возвращает None.
    """
    try:
        file_list = None
        file_list = [Path_+'/'+x.lower() for x in ListDir(Path_)]
        file_list = [x for x in file_list if IsFile(x)]
        return file_list
    except:
        log.fatal(u'Ошибка определения списка файлов директории %s' % Path_)
        return None


def GetFilesByExt(Path_, Ext_):
    """
    Функция возвращает список всех файлов в директории с указанным расширением.
    @param Path_: Путь.
    @param Ext_: Расширение, например '.pro'.
    @return: В случае ошибки возвращает None.
    """
    file_list = None
    try:
        if Ext_[0] != '.':
            Ext_ = '.'+Ext_
        Ext_ = Ext_.lower()

        file_list = [Path_+'/'+file_name for file_name in ListDir(Path_)]
        file_list = [file_name for file_name in file_list if IsFile(file_name) and
                           (SplitExt(file_name)[1].lower() == Ext_)]
        return file_list
    except:
        log.fatal(u'Ошибка определения списка файлов по расширению %s из директории %s: %s' % (Ext_,
                                                                                               Path_, file_list))
        return None


def icCleanFileExt(Path_, Ext_):
    """
    Функция УДАЛЯЕТ РЕКУРСИВНО В ПОДДИРЕКТОРИЯХ
        все файлы в директории с заданным расширением.
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
        log.fatal(u'Ошибка рекурсивного удаления файлов')
        return False


def icRelativePath(Path_):
    """
    Относительный путь.
    @param Path_: Путь.
    """
    Path_ = Path_.replace('/', '\\').lower()
    cur_dir = os.getcwd().lower()
    return Path_.replace(cur_dir, '.')


def icAbsolutePath(Path_):
    """
    Абсолютный путь.
    @param Path_: Путь.
    """
    try:
        Path_ = AbsPath(Path_)
        Path_ = Path_.replace('\\', '/').lower()
        return Path_
    except:
        log.fatal(u'Path: <%s>' % Path_)
        return Path_


def RelativePath(Path_, CurDir_=None):
    """
    Относительный путь. Путь приводится к виду Unix.
    @param Path_: Путь.
    @param CurDir_: Текущий путь.
    """
    if CurDir_ is None:
        CurDir_ = DirName(ic.ic_run.ic_user.icGet('PRJ_DIR')).replace('\\', '/').lower()
    if CurDir_:
        Path_ = Path_.replace('\\', '/').lower()
        return Path_.replace(CurDir_, '.')
    return Path_


def AbsolutePath(Path_, CurDir_=None):
    """
    Абсолютный путь. Путь приводится к виду Unix.
    @param Path_: Путь.
    @param CurDir_: Текущий путь.
    """
    try:
        # Нормализация текущего пути
        if CurDir_ is None:
            CurDir_ = DirName(ic.ic_run.ic_user.icGet('PRJ_DIR'))
        CurDir_ = CurDir_.replace('\\', '/').lower()
        if CurDir_[-1] != '/':
            CurDir_ += '/'
        # Коррекция самого пути
        Path_ = Path_.replace('\\', '/').lower()
        Path_ = Path_.replace('./', CurDir_)
        return Path_
    except:
        log.fatal(u'ОШИБКА: AbsolutePath: <%s>' % Path_)
        return Path_


def PathFile(Path_, File_):
    """
    Корректное представление общего имени файла.
    @param Path_: Путь.
    @param File_: Имя файла.
    """
    File_ = File_.replace('/', '\\')
    Path_ = Path_.replace('/', '\\')
    relative_path = icRelativePath(Path_).replace('/', '\\')
    # Этот путь уже присутствует в имени файла
    if File_.find(Path_) != -1 or File_.find(relative_path) != -1:
        return File_
    return (relative_path+'\\'+File_).replace('\\\\', '\\')


def NormPathWin(Path_):
    """
    Приведение пути к виду Windows.
    """
    if Path_.find(' ') > -1 and Path_[0] != '"' and Path_[-1] != '"':
        return '"'+NormPath(Path_)+'"'
    else:
        return NormPath(Path_)


def NormPathUnix(Path_):
    """
    Приведение пути к виду UNIX.
    """
    return NormPath(Path_).replace('\\', '/')


def SamePathWin(Path1_, Path2_):
    """
    Проверка,  Path1_==Path2_.
    """
    return bool(NormPathWin(Path1_) == NormPathWin(Path2_))


def CopyDir(Dir_, ToDir_, ReWrite_=False):
    """
    Функция папку Dir_ в папку ToDir_
        со всеми внутренними поддиректориями и файлами.
    @param Dir_: Папка/директория,  которая копируется.
    @param ToDir_: Папка/директория, в которую копируется Dir_.
    @param ReWrite_: Указание перезаписи директории, если она
        уже существует.
    @return: Функция возвращает результат выполнения операции True/False.
    """
    try:
        to_dir = ToDir_+'/'+BaseName(Dir_)
        if Exists(to_dir) and ReWrite_:
            shutil.rmtree(to_dir, 1)
        shutil.copytree(Dir_, to_dir)
        return True
    except:
        log.fatal(u'Ошибка копирования папки <%s> в папку <%s>' % (Dir_, ToDir_))
        return False


def CloneDir(Dir_, NewDir_, ReWrite_=False):
    """
    Функция переносит все содержимое папки Dir_ в
        папку с новым именем NewDir_.
    @param Dir_: Папка/директория,  которая копируется.
    @param NewDir_: Новое имя папки/директории.
    @param ReWrite_: Указание перезаписи директории, если она
        уже существует.
    @return: Функция возвращает результат выполнения операции True/False.
    """
    try:
        if Exists(NewDir_) and ReWrite_:
            shutil.rmtree(NewDir_, 1)
        MakeDirs(NewDir_)
        for sub_dir in GetSubDirs(Dir_):
            shutil.copytree(sub_dir, NewDir_)
        for file_name in GetFiles(Dir_):
            icCopyFile(file_name, NewDir_+'/'+BaseName(file_name))
        return True
    except:
        log.fatal(u'Ошибка переноса содержимого папки <%s> в папку <%s>' % (Dir_, NewDir_))
        return False


def IsSubDir(Dir1_, Dir2_):
    """
    Функция проверяет, является ли директория Dir1_
        поддиректорией Dir2_.
    @return: Возвращает True/False.
    """
    dir1 = AbsPath(Dir1_)
    dir2 = AbsPath(Dir2_)
    if dir1 == dir2:
        return True
    else:
        sub_dirs = [path for path in [dir2+'\\'+name for name in ListDir(dir2)] if IsDir(path)]
        for cur_sub_dir in sub_dirs:
            find = IsSubDir(Dir1_, cur_sub_dir)
            if find:
                return find
    return False


def genDefaultBakFileName():
    """
    Генерация имени бак файла по текущему времени.
    """
    return time.strftime('_%d_%m_%Y_%H_%M_%S.bak',
                         time.localtime(time.time()))


def getFilesByMask(FileMask_):
    """
    Список файлов по маске.
    @param FileMask_: Маска файлов. Например C:\Temp\*.dbf.
    @return: Возвращает список строк-полных путей к файлам.
        В случае ошибки None.
    """
    return [AbsPath(file_name) for file_name in glob.glob(FileMask_)]


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
    return icCopyFile(FileName_, DestDir_+'/'+BaseName(FileName_), Rewrite_)


def delAllFilesFilter(DelDir_, *Filter_):
    """
    Удаление всех файлов из папки с фильтрацией по маске файла.
        Удаление рекурсивное по поддиректориям.
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
            del_files = getFilesByMask(DelDir_+'/'+file_mask)
            for del_file in del_files:
                Remove(del_file)
        return True
    except:
        log.fatal(u'Ошибка в функции ic_file.delAllFilesFilter')
        return None


def getPythonDir():
    """
    Папка в которую установлен Python.
    """
    return DirName(sys.excutable)


def getHomeDir():
    """
    Папка HOME.
    """
    if sys.platform[:3].lower() == 'win':
        home_dir = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
        home_dir = home_dir.replace('\\', '/')
    else:
        home_dir = os.environ['HOME']
    return home_dir


def test():
    #  Тестируем icCopyFileByMask
    icCopyFilesByMask('c:/!/1/Пример*.*', 'c:/!/2/pr*.*')


if __name__ == "__main__":
    test()
