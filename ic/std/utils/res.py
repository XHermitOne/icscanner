#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций работы с ресурсными файлами.
"""

import os
import os.path
import cPickle

from ic.std.log import log

from . import textfunc

# Протокол хранения сериализованных объектов модулем cPickle
# ВНИМАНИЕ!!! PICKLE_PROTOCOL = 1,2 использовать нельзя - ресурсы не востанавливаются
PICKLE_PROTOCOL = 0

# Буфер транслированных ресурсных файлов
Buff_readAndEvalFile = {}


def loadResourceFile(filename, dictRpl={}, bRefresh=False, *arg, **kwarg):
    """
    Загрузить ресурс из файла. Функция читает файл и выполняет его.
    @type filename: C{string}
    @param filename: Имя ресурсного файла.
    @type dictRpl: C{dictionary}
    @param dictRpl: Словарь замен.
    @type bRefresh: C{bool}
    @param bRefresh: Признак того, что файл надо перечитать даже если он
        буферезирован.
    """
    obj = None
    filename = filename.strip()
    try:
        # Проверяем есть ли в буфферном файле такой объект, если есть, то его и возвращаем
        if not bRefresh and filename in Buff_readAndEvalFile:
            log.debug(' '*3+'[b] '+'Return from buffer file: <%s>' % filename)
            return Buff_readAndEvalFile[filename]

        nm = os.path.basename(filename)
        pt = nm.find('.')
        if pt >= 0:
            filepcl = os.path.dirname(filename) + '/' + nm[:pt] + '_pkl' + nm[pt:]
        else:
            filepcl = os.path.dirname(filename) + '/' + nm +'_pkl'

        # Проверяем нужно ли компилировать данную структуру по следующим признакам:
        # наличие скомпилированного файла, по времени последней модификации.
        try:
            if (os.path.isfile(filepcl) and not os.path.isfile(filename)) or \
                    (os.path.getmtime(filename) < os.path.getmtime(filepcl)):
                # Пытаеся прочитать сохраненную структуру если время последней
                # модификации текстового представления меньше, времени
                # последней модификации транслированного варианта.
                fpcl = None
                try:
                    fpcl = open(filepcl)
                    obj = cPickle.load(fpcl)
                    fpcl.close()
                    # Сохраняем объект в буфере
                    Buff_readAndEvalFile[filename] = obj
                    log.debug('   [+] Load from: %s' % filepcl)
                    return obj
                except IOError:
                    log.error('   [-] readAndEvalFile: Open file <%s> error.' % filepcl)
                except:
                    if fpcl:
                        fpcl.close()
        except:
            pass
        # Пытаемся прочитать cPickle, если не удается считаем, что в файле
        # хранится текст. Читаем его, выполняем, полученный объект сохраняем
        # на диске для последующего использования
        if os.path.isfile(filename):
            try:
                fpcl = open(filename)
                obj = cPickle.load(fpcl)
                fpcl.close()
                # Сохраняем объект в буфере
                Buff_readAndEvalFile[filename] = obj
                log.debug('   [+] Load file <%s> cPickle Format.' % filename)
                return obj
            except Exception, msg:
                log.error('   [*] Non cPickle Format file <%s>. Try to compile text' % filename)

        # Открываем текстовое представление, если его нет, то создаем его
        f = open(filename, 'rb')
        txt = f.read().replace('\r\n', '\n')
        f.close()
        for key in dictRpl:
            txt = txt.replace(key, dictRpl[key])

        # Выполняем
        obj = eval(txt)
        # Сохраняем объект в буфере
        Buff_readAndEvalFile[filename] = obj

        # Сохраняем транслированный вариант
        fpcl = open(filepcl, 'w')
        log.debug('Create cPickle <%s>' % filepcl)
        cPickle.dump(obj, fpcl, PICKLE_PROTOCOL)
        fpcl.close()
    except IOError:
        log.error('   [*] Open file <%s> error.' % filename)
        obj = None
    except:
        log.error('   [*] Translation file <%s> error.' % filename)
        obj = None

    return obj


def loadResource(FileName_):
    """
    Получить ресурс в ресурсном файле.
    @param FileName_: Полное имя ресурсного файла.
    """
    # Сначала предположим что файл в формате Pickle.
    struct = loadResourcePickle(FileName_)
    if struct is None:
        # Но если он не в формате Pickle, то скорее всего в тексте.
        struct = loadResourceText(FileName_)
    if struct is None:
        # Но если не в тексте но ошибка!
        log.warning(u'Ошибка формата файла %s.' % FileName_)
        return None
    return struct


def loadResourcePickle(FileName_):
    """
    Получить ресурс из ресурсного файла в формате Pickle.
    @param FileName_: Полное имя ресурсного файла.
    """
    if os.path.isfile(FileName_):
        try:
            f = None
            f = open(FileName_)
            struct = cPickle.load(f)
            f.close()
            return struct
        except:
            if f:
                f.close()
            log.error(u'Ошибка чтения файла <%s>.' % FileName_)
            return None
    else:
        log.warning(u'Файл <%s> не найден.' % FileName_)
        return None


def loadResourceText(FileName_):
    """
    Получить ресурс из ресурсного файла в текстовом формате.
    @param FileName_: Полное имя ресурсного файла.
    """
    if os.path.isfile(FileName_):
        try:
            f = None
            f = open(FileName_)
            txt = f.read().replace('\r\n', '\n')
            f.close()
            return eval(txt)
        except:
            if f:
                f.close()
            log.error(u'Ошибка чтения файла <%s>.' % FileName_)
            return None
    else:
        log.warning(u'Файл <%s> не найден.' % FileName_)
        return None


def saveResourcePickle(FileName_, Resource_):
    """
    Сохранить ресурс в файле в формате Pickle.
    @param FileName_: Полное имя ресурсного файла.
    @param Resource_: Словарно-списковая структура спецификации.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        f = None

        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(FileName_)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(FileName_, 'w')
        cPickle.dump(Resource_, f)
        f.close()
        log.info(u'Файл <%s> сохранен в формате Pickle.' % FileName_)
        return True
    except:
        if f:
            f.close()
        log.error(u'Ошибка сохраненения файла <%s> в формате Pickle.' % FileName_)

        return False


def saveResourceText(FileName_, Resource_):
    """
    Сохранить ресурс в файле в текстовом формате.
    @param FileName_: Полное имя ресурсного файла.
    @param Resource_: Словарно-списковая структура спецификации.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        f = None
        # Если необходимые папки не созданы, то создать их
        dir_name = os.path.dirname(FileName_)
        try:
            os.makedirs(dir_name)
        except:
            pass

        f = open(FileName_, 'w')
        text = textfunc.StructToTxt(Resource_)
        f.write(text)
        f.close()
        log.info(u'Файл <%s> сохранен в текстовом формате.' % FileName_)
        return True
    except:
        if f:
            f.close()
        log.error(u'Ошибка сохраненения файла <%s> в текстовом формате.' % FileName_)
        return False
