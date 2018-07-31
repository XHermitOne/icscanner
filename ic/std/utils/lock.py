#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Библиотека блокировок.
"""

# --- Подключение пакетов ---
import os

from . import ic_file

from ic.std.log import log

__version__ = (0, 0, 1, 2)

# --- Константы ---
# Расширение файла блокировки
LOCK_FILE_EXT = '.lck'


# --- Функции ---
def LockFile(FileName_, LockRecord_=None):
    """
    Блокировка файла.
    @param FileName_: Полное имя блокируемого файла.
    @param LockRecord_: Запись блокировки.
    @return: Возвращает кортеж:
        (результат выполения операции,запись блокировки).
    """
    lock_file_flag = False  # Флаг блокировки файла
    lock_rec = LockRecord_
    
    # Сгенерировать имя файла блокировки
    lock_file = ic_file.SplitExt(FileName_)[0]+LOCK_FILE_EXT
    # Если файл не заблокирован, то заблокировать его
    if not ic_file.IsFile(lock_file):
        # Создать все директории для файла блокировки
        lock_dir = ic_file.DirName(lock_file)
        if not ic_file.IsDir(lock_dir):
            ic_file.MakeDirs(lock_dir)
        
        # Генерация файла-флага блокировки
        # ВНИМАНИЕ! Создавать файл надо на самом нижнем уровне!
        f = None
        try:
            #  Попытка создать файл
            f = os.open(lock_file, os.O_CREAT | os.O_EXCL, 0777)
        except OSError:
            #  Уже есть файл. Т.Е. уже заблокирован
            lock_file_flag = True
            # Прочитать кем хоть заблокирован
            if f:
                # Закрыть сначала
                os.close(f)
            lock_rec = ReadLockRecord(lock_file)
        else:
            #  выполнено без ошибки
            #  Записать запись блокировки в файл
            if LockRecord_ is not None:
                # Закрыть сначала
                os.close(f)
                # Открыть для записи
                f = os.open(lock_file, os.O_WRONLY , 0777)
                os.write(f, str(LockRecord_))
            os.close(f)
    else:
        # Если файл заблокирован
        lock_file_flag = True
        lock_rec = ReadLockRecord(lock_file)

    return not lock_file_flag, lock_rec


def ReadLockRecord(LockFile_):
    """
    Прочитать запись блокировки из файла блокировки.
    @param LockFile_: Имя файла блокировки.
    @return: Возвращает запись блокировки или None в случае ошибки.
    """
    f = None
    try:
        lock_file = None
        lock_rec = None
        # На всякий случай преобразовать
        lock_file = ic_file.SplitExt(LockFile_)[0]+LOCK_FILE_EXT
        # Если файла не существует, тогда и нечего прочитать
        if not ic_file.Exists(lock_file):
            return None
        # Открыть для чтения
        f = os.open(lock_file, os.O_RDONLY, 0777)
        lock_rec = os.read(f, 65535)
        os.close(f)
        try:
            # Если храниться какая-либо структура,
            # то сразу преобразовать ее
            return eval(lock_rec)
        except:
            return lock_rec
    except:
        if f:
            os.close(f)
        log.fatal(u'Чтение записи блокировки %s' % lock_file)
        return None


def IsLockedFile(FileName_):
    """
    Проверка блокировки файла.
    @param FileName_: Имя файла.
    @return: Возвращает результат True/False.
    """
    # Сгенерировать имя файла блокировки
    lock_file = ic_file.SplitExt(FileName_)[0]+LOCK_FILE_EXT
    return ic_file.IsFile(lock_file)


def ComputerName():
    """
    Имя хоста.
    @return: Получит имя компа в сети.
    """
    if 'COMPUTERNAME' in os.environ:
        return os.environ['COMPUTERNAME']
    else:
        import socket
        return socket.gethostname()


def UnLockFile(FileName_, **If_):
    """
    Разблокировать файл.
    @param FileName_: Имя файла.
    @param If_: Условие проверки разблокировки.
        Ключ записи блокировки=значение.
        Проверка производится по "И".
        Если такого ключа в записи нет,
        то его значение берется None.
    @return: Возвращает результат True/False.
    """
    # Сгенерировать имя файла блокировки
    lock_file = ic_file.SplitExt(FileName_)[0]+LOCK_FILE_EXT
    if ic_file.IsFile(lock_file):
        if If_:
            lck_rec = ReadLockRecord(lock_file)
            # Если значения по указанным ключам равны, то все ОК
            can_unlock = bool(len([key for key in If_.keys() if lck_rec.setdefault(key, None) == If_[key]]) == len(If_))
            if can_unlock:
                # Ресурс можно разблокировать
                ic_file.Remove(lock_file)
            else:
                # Нельзя разблокировать файл
                return False
        else:
            # Ресурс можно разблокировать
            ic_file.Remove(lock_file)
    return True


def _UnLockFileWalk(ComputerName_, CurDir_, CurNames_):
    """
    Вспомогательная функция разблокировки файла на уровне каталога по
        имени компьютера. Используется в функции os.path.walk().
    @param ComputerName_: Имя компьютера файлы которого нужно раблокировать.
    @param CurDir_: Текущий директорий.
    @param CurNames_: Имена поддиректорий и файлов в текущей директории.
    """
    # Отфильтровать только файлы блокировок
    lock_files = [x for x in [ic_file.Join(CurDir_, x) for x in CurNames_] if ic_file.IsFile(x) and ic_file.SplitExt(x)[1] == LOCK_FILE_EXT]
    # Выбрать только свои файлы-блокировки
    for cur_file in lock_files:
        if ReadLockRecord(cur_file)['owner'] == ComputerName_:
            ic_file.Remove(cur_file)


def UnLockAllFile(LockDir_, ComputerName_=None):
    """
    Разблокировка всех файлов.
    @param LockDir_: Директория блокировок.
    @param ComputerName_: Имя компьютера файлы которого нужно раблокировать.
    @return: Возвращает результат True/False.
    """
    if not ComputerName_:
        ComputerName_ = ComputerName()
    return ic_file.Walk(LockDir_, _UnLockFileWalk, ComputerName_)


class icLockSystem:
    """
    Система блокировки произвольных ресурсов.
    """
    def __init__(self, LockDir_=None):
        """
        Конструктор.
        @param LockDir_: Папка блокировки.
        """
        if LockDir_ is None:
            LockDir_ = ic_lock.lockDir
        
        self._LockDir = LockDir_
        
    # --- Папочные блокировки ---
    def lockDirRes(self, LockName_):
        """
        Поставить блокировку в виде директории.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к директории.
        """
        pass
        
    def unLockDirRes(self, LockName_):
        """
        Убрать блокировку в виде директории.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к директории.
        """
        pass

    # --- Файловые блокировки ---
    def _getLockFileName(self, LockName_):
        """
        Определитьимя файла блокировки по имени блокировки.
        @param LockName_: Имя блокировки.
        """
        lock_file_name = os.path.join(self._LockDir, 'default'+LOCK_FILE_EXT)
        try:
            if isinstance(LockName_, list):
                lock_name = LockName_[-1]
            elif isinstance(LockName_, str):
                lock_name = ic_file.SplitExt(ic_file.BaseName(LockName_))[0]
            lock_file_name = os.path.join(self._LockDir, lock_name+LOCK_FILE_EXT)
            return lock_file_name
        except:
            log.fatal(u'Ошибка определения имени файла блокировки %s %s' % (self._LockDir, LockName_))
        return lock_file_name
        
    def lockFileRes(self, LockName_, LockRec_=None):
        """
        Поставить блокировку в виде файла.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к файлу.
        @param LockRec_: Запись блокировки.
        """
        lock_file_name = self._getLockFileName(LockName_)
        if LockRec_ is None:
            LockRec_ = {'owner': ComputerName()}
        return LockFile(lock_file_name, LockRec_)
        
    def unLockFileRes(self, LockName_):
        """
        Убрать блокировку в виде файла.
        @param LockName_: Имя блокировки.
            М.б. реализовано в виде списка имен,
            что определяет путь к файлу.
        """
        lock_file_name = self._getLockFileName(LockName_)
        return UnLockFile(lock_file_name)

    def isLockFileRes(self, LockName_):
        """
        Существует ли файловая блокировка с именем.
        @param LockName_: Имя блокировки.
        """
        lock_file_name = self._getLockFileName(LockName_)
        return IsLockedFile(lock_file_name)
    
    def getLockRec(self, LockName_):
        """
        Определить запись блокировки.
        @param LockName_: Имя блокировки.
        """
        lock_file_name = self._getLockFileName(LockName_)
        return ReadLockRecord(lock_file_name)
    
    # --- Общие функции блокировки ---
    def isLockRes(self, LockName_):
        """
        Существует ли блокировка с именем.
        @param LockName_: Имя блокировки.
        """
        pass
        
    def unLockAllMy(self):
        """
        Разблокировать все мои блокировки.
        """
        return UnLockAllFile(self._LockDir, ComputerName())
