# ! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций работы с ресурсными файлами системы.
"""

# Подключение библиотек
import copy
import os.path
from . import util

from ic.std.log import log

try:
    from services.ic_std.imglib import common
except:
    log.error(u'Import Error imglib')

from . import ic_res

#   Указатель на пользовательское хранилище
isUserObjectStorage = None

__version__ = (1, 1, 1, 2)

IC_DOC_PATH = os.path.join(os.getcwd(), 'ic', 'doc', 'html')


# --- Функции определения ресурсных файлов системы ---
def icGetResPath():
    """
    Возвращает путь до директории, где располагаются ресурсные файлы
    """
    return ic.ic_run.ic_user.icGet('SYS_RES')


def IsDebugMode():
    if ic.ic_run.ic_user.icIs('DEBUG_MODE'):
        return ic.ic_run.ic_user.icGet('DEBUG_MODE')
    else:
        return False


def icGetUserPath():
    """
    Возвращает путь до директории пользователя.
    """
    userName = ic.ic_run.ic_user.icGet('UserName')
    path = icGetResPath()

    if not userName:
        return None
    
    res = icGetRes(userName, 'acc', path)
    
    if res:
        user_path = res['local_dir']
        return user_path

    return None
    

def icSetUserVariable(varName, value, subsys=''):
    """
    Функция устанавливает переменную пользователя.
    
    @type varName: C{string}
    @param varName: Имя переменной.
    @type value: C{string}
    @param value: Значение переменной.
    @type subsys: C{string}
    @param subsys: Имя подсистемы
    """
    res_path = icGetUserPath()
    if not res_path:
        return None
    
    #   По необходимости создаем хранилище
    storage = ic.storage.storesrc.icTreeDirStorage(res_path)
    storage.Open()
    keyObj = del_lock.GetMyHostName()+'Property'
   
    #   По необходимости создаем файл
    if keyObj not in storage:
        storage[keyObj] = ic.storage.storesrc.icFileStorage()

    storage[keyObj][varName] = value
    storage.Close()
    return True


def icGetUserVariable(varName, subsys=''):
    """
    Функция устанавливает переменную пользователя.
    
    @type varName: C{string}
    @param varName: Имя переменной.
    @type value: C{string}
    @param value: Значение переменной.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    """
    res_path = icGetUserPath()
    
    if not res_path:
        return None

    #   По необходимости создаем хранилище
    storage = ic.storage.storesrc.icTreeDirStorage(res_path)
    storage.Open()

    keyObj = del_lock.GetMyHostName()+'Property'
    result = None
    
    #   По необходимости создаем файл
    if keyObj in storage and varName in storage[keyObj]:
        result = storage[keyObj][varName]
    
    storage.Close()
    return result


def icGetCfgFrame():
    """
    Возвращает путь до директории, где располагаются ресурсные файлы
    """
    appx = ic.ic_run.ic_user.icRef('CFG_APP')
    return appx.appFrame


def icGetSubsysResPaths():
    """
    Возвращает список путей до всех подсистем.
    """
    paths = ic.ic_run.ic_user.icGet('SUBSYS_RES')
    
    if not paths:
        paths = [icGetResPath()]
        
    return paths


def icGetICPath():
    """
    Возвращает путь до пакета ic.
    """
    return common.icpath


def icGetUserClassesPath():
    return icGetICPath()+'/components/user'


def icGetHlpPath():
    """
    Возвращает путь до директории, где располагаются файлы документации
    """
    return IC_DOC_PATH


def icGetResFileName(Ext_='tab'):
    """
    Ресурсный файл.
    @return: Функцмя возвращает полное имя ресурсного файла по его расширению.
    """
    res_file = icGetResPath()+'resource.'+Ext_
    res_file = res_file.replace('/', '\\')
    return res_file

# --- Функции наследования ресурсов ---


def inherit(prnt_res, resource, lstExcept=[]):
    """
    Наследуем атрибуты родительского описания.
    
    @type prnt_res: C{dictionary}
    @param prnt_res: Родительское описание.
    @type resource: C{dictionary}
    @param resource: Описание потомка.
    @type lstExcept: C{list}
    @param lstExcept: Список не наследуемых атрибутов.
    @rtype: C{dictionary}
    @return: Возвращает наследованное ресурсное описание.
    """
    
    for key, attr in resource.items():
        if key not in lstExcept and not attr and key in prnt_res:
            resource[key] = prnt_res[key]
    
    return resource


def inheritDataClass(prnt_res, resource):
    """
    Функция наследования ресурсных описаний классов данных.
    
    @type prnt_res: C{dictionary}
    @param prnt_res: Родительское описание.
    @type resource: C{dictionary}
    @param resource: Описание потомка.
    @rtype: C{dictionary}
    @return: Возвращает наследованное ресурсное описание класса данных.
    """
    #   Наследуем атрибуты родительского класса данных
    inherit(prnt_res, resource, ['parent'])
                                    
    #   Наследуем описания полей
    #   1. Создаем словарь схемы дочернего ресурса
    res_dict = {}
    
    for fld in resource['scheme']:
        res_dict[fld['name']] = fld
    
    for fld in prnt_res['scheme']:
        
        #   Если имена совпали, то используем наследование
        if fld['name'] in res_dict.keys():
            inherit(fld, res_dict[fld['name']])
        
        #   В противном случае добавляем описание поля в схему
        else:
            resource['scheme'].append(fld)
        
    return resource


def buildDataClassRes(resource, nameRes='resource'):
    """
    Собирает ресурсное описание класса данных с испольозованием механизма
    наследования.
    
    @type resource: C{dictionary}
    @param resource: Ресурсное описание без наследования.
    @type nameRes: C{string}
    @param mameRes: Имя ресурсного файла. Если оно не указано, то используется 'resource'. В
        старых версиях все ресурсы одного типа хранились в одном файле, поэтому этот параметр не
        использовался.
    """
    if not isinstance(resource, dict) or 'parent' not in resource:
        return resource
    
    #   Организуем наследование классов данных
    prnt_name = resource['parent']
    tableName = None
    
    while prnt_name:
        #   Выделяем имя подсистемы
        if '/' in prnt_name:
            subsys, clsName = prnt_name.split('/')
            subsys_path = getSubsysPath(subsys)
                        
            prnt_res = icGetRes(clsName, 'tab', subsys_path, bCopy=True, nameRes=nameRes)
        else:
            prnt_res = icGetRes(prnt_name, 'tab', bCopy=True, nameRes=nameRes)
            
        if prnt_res:
            
            if not tableName and resource['type'] == 'icQuery' and prnt_res['type'] == 'icDataClass':
                tableName = prnt_res['name']
                
            resource = inheritDataClass(prnt_res, resource)
            prnt_name = prnt_res['parent']
            
        else:
            break

    #   Для запроосов в атрибут 'parent' записываем имя класса данных, от которого наследуется
    #   запрос. Для классов данных None.
    resource['parent'] = tableName
    return resource


# --- Работа с ресурсами ---
def icGetRes(className, ext='tab', pathRes=None, bCopy=True, bRefresh=False, nameRes='resource'):
    """
    Возврвщает ресурсное описание объекта. После того как функция находит
    нужное ресурсное описание в служебном атрибуте ресурса '__file_res' прописывается
    полный путь до файла ресурса, где он был найден.
    
    @type className: C{string}
    @param className: Имя ресурса.
    @type ext: C{string}
    @param ext: Расширения ресурсного файла для данного ресурса.
    @type pathRes: C{string}
    @param pathRes: Имя ресурсного файла. Если путь не указан, то нужный ресурсный файл
        последовательно ищется во всех папках подсистем, начиная с папки текущего проекта.
    @type bCopy: C{bool}
    @param bCopy: Признак указывающий, что надо возвращать копию ресурса, в противном
        случае возвращается указатель на ресурс. Поскольку он буферезируется то
        с ним необходимо очень акуратно работать.
    @type bRefresh: C{bool}
    @param bRefresh: Признак того, что ресурс надо перечитать даже если он
        буферезирован.
    @type nameRes: C{string}
    @param nameRes: Имя ресурсного файла. Если оно не указано, то используется 'resource'. В
        старых версиях все ресурсы одного типа хранились в одном файле, поэтому этот параметр не
        использовался.
    @rtype: C{dictionary}
    @return: Ресурсное описание объекта. None если ресурс не найден.
    """
    if not pathRes:
        paths = icGetSubsysResPaths()
    else:
        paths = [pathRes]

    #   Перебираем все пути подсистем
    resource = None

    for pathRes in paths:
        fileRes = (pathRes+'/'+nameRes+'.'+ext).replace('\\', '/').replace('//', '/')
        
        #   Подготавливаем словарь замен
        if os.path.isfile(fileRes):
            #   Читаем ресурсное описание
            res = util.readAndEvalFile(fileRes, bRefresh = bRefresh)
    
            try:
                if bCopy and className:
                    resource = copy.deepcopy(res[className])
                elif className:
                    resource = res[className]
        
                #   Организуем наследование классов данных
                if ext == 'tab':
                    resource = buildDataClassRes(resource)

                resource['__file_res'] = fileRes
                return resource
                            
            except KeyError:
                log.fatal(u'Don\'t find component <%s> in resource <%s>' % (className, fileRes))
        else:
            log.warning(u'icGetRes: resource file <%s> not found' % fileRes)

    MsgBox(None, u'Описание компонента <%s> в ресурсных файлах не найдено' % className)
    return None
    

def RefreshResUUID(res, prnt_res, new_uuid):
    """
    Обновляет UUID ресурса. Для некоторых ресурсов (GridCell) обновление надо проводить в
    родительском ресурсе, так как они описывают один состовной объект.
    
    @type res: C{dictionary}
    @param res: Ресурсное описание компонента.
    @type prnt_res: C{dictionary}
    @param prnt_res: Ресурсное описание родительского компонента.
    @type new_uuid: C{string}
    @param new_uuid: Новый uuid компонента.
    """
    if res['type'] == 'GridCell' and prnt_res:
        prnt_res['_uuid'] = new_uuid
    else:
        res['_uuid'] = new_uuid


def delResServiceInfo(res):
    """
    Удаляет служебную информацию из ресурса.
    """
    if not res or not isinstance(res, dict):
        return False

    for key, val in res.items():
        if key.startswith('__'):
            res.pop(key)
        elif key in ['cell_attr', 'label_attr'] and isinstance(val, dict):
            delResServiceInfo(val)
        elif key in ['child', 'win1', 'win2', 'cols'] and isinstance(val, list):
            for el in val:
                delResServiceInfo(el)
        elif key in ['win1', 'win2'] and isinstance(val, dict):
            delResServiceInfo(val)


def genNextVersion(version=None):
    """
    По старой версии генерирует новую.
    """
    if version:
        lst = list(version)
        ver = reduce(lambda x, y: x*10+y, lst)
        return [int(s) for s in str(ver+1)]
    else:
        return 1, 0, 0, 1


def genClassFromRes(className, res, version=None):
    """
    Генерирует класс по ресурсу.
    """
    #   Удаляем служебную информацию
    delResServiceInfo(res)
    version = genNextVersion(version)
        
    class_txt = '''#!/usr/bin/env python
# -*- coding: cp1251 -*-

import wx
import services.ic_std.components.icResourceParser as prs
import services.ic_std.utils.util as util
import services.ic_std.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK

#   Ресурсное описание класса
resource = %s

#   Версия объекта
__version__ = %s
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = '%s'

class %s(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        """
        Конструктор интерфейса.
        """
        #
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс %s.
    """
    from ic.components import ic_stdtestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
    
    '''
    class_txt = class_txt % (str(res), str(version), className, className, className)
    
    return class_txt


def MyExec(s):
    exec s


def getICObjectResource(path):
    """
    Возвращает ресурсное описание и имя класса системного объекта.
    """
    try:
        #   Импортируем модуль
        mod = util.icLoadSource('modulRes', path)
        res = mod.resource
        
        #   Читаем имя класса
        try:
            className = mod.ic_class_name
        except:
            className = 'icObjectClass'
        
        #   Читаем версию
        try:
            version = mod.__version__
        except:
            version = (1, 0, 0, 1)
        
        del mod
        
        if isinstance(res, dict):
            return res, className, version
    except:
        log.fatal(u'Import Error modul=<%s>' % path)
        
    return None, None, None


def saveICObject(path, className, res):
    """
    Генерирует по ресурсу питоновский класс и сохраняет в нужном модуле.
    
    @type path: C{string}
    @param path: Путь до файла.
    @type className: C{string}
    @param className: Имя класса.
    @type res: C{dictionary}
    @param res: Ресурсное описание.
    """
    
    text = genClassFromRes(className, res)
    f = open(path, 'w')
    f.write(text)
    f.close()


def updateICObject(path, className, res, version=None):
    """
    Обновляет ресурсное описание питоновского класса.
    
    @type path: C{string}
    @param path: Путь до файла.
    @type className: C{string}
    @param className: Имя класса.
    @type res: C{dictionary}
    @param res: Ресурсное описание.
    """
    #   Читаем текст файла
    f = open(path, 'rb')
    text = f.read()
    f.close()
    
    #   Обновляем текст
    version = genNextVersion(version)
    n1 = text.find('###BEGIN')
    n2 = text.find('###END')
    
    text = text[:n1] + '''###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource = %s

#   Версия объекта
__version__ = %s
''' % (str(res), str(tuple(version))) + text[n2:]
    
    #   Сохраняет текст - стандартный метод сохраняет с разделителями системы '\r\n'.
    f = open(path, 'wb')
    f.write(text)
    f.close()


def getSubsysPath(subsys=None):
    """
    Функция по имени подсистемы определяет полный путь до подсистемы.
    
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    """
    sys_path = icGetSubsysResPaths()[0].replace('\\', '/')
    
    if subsys:
        return '/'.join(sys_path.split('/')[:-1])+'/'+subsys
    else:
        return sys_path


def method(id_meth, subsys, esp=locals(), **params):
    """
    Находит и выполняет метод подсистемы.
    
    @type id_meth: C{string}
    @param id_meth: Идентификатор метода.
    @type subsys: C{string}
    @param subsys: Имя подсистемы.
    @type params: C{dict}
    @param params: Дополнительные параметры метода.
    """
    if subsys:
        subsys_path = getSubsysPath(subsys)
    else:
        subsys_path = None
    
    evalSpace = esp
    
    for par, val in params.items():
        evalSpace[par] = val
    
    meth_expr = icGetRes(id_meth, 'mth', subsys_path, False)
    
    if meth_expr and isinstance(meth_expr, dict) and 'body' in meth_expr:
        keyExpr = str(id_meth)+'_'+str(subsys)+'_method'
        ret, val = util.ic_eval(meth_expr['body'], 0, evalSpace,
                                '<method>=%s, <subsys>=%s' % (id_meth, subsys),
                                compileKey=keyExpr)
        if ret:
            return val
            
    elif subsys_path:
        log.warning(u'Method <%s> don\'t find in subsys %s' % (id_meth, subsys))
    else:
        log.warning(u'Method <%s> don\'t find in subsyses' % id_meth)
        
    return None


def icSaveRes(className, ext, pathRes=None, nameRes='resource', resData=None):
    """
    Сохранить ресурсное описание объекта.
    @type className: C{string}
    @param className: Имя ресурса.
    @type ext: C{string}
    @param ext: Расширения ресурсного файла для данного ресурса.
    @type pathRes: C{string}
    @param pathRes: Имя ресурсного файла. Если путь не указан, то ресурсный файл
        в папке текущего проекта.
    @type nameRes: C{string}
    @param nameRes: Имя ресурсного файла. Если оно не указано, то используется 'resource'. В
        старых версиях все ресурсы одного типа хранились в одном файле, поэтому этот параметр не
        использовался.
    @rtype: C{dictionary}
    @return: Ресурсное описание объекта. None если ресурс не найден.
    """
    if not pathRes:
        pathRes = ic.ic_run.ic_user.icGet('PRJ_DIR')
    fileResName = (pathRes+'/'+nameRes+'.'+ext).replace('\\', '/').replace('//', '/')

    return ic_res.SaveResourcePickle(fileResName, {className: resData})
        

if __name__ == '__main__':
    prnt_res = {'1': 1, '3': 3, 'scheme': [{'name': 1, 'p1': 1}, {'name': 2, 'p2': 'p'}]}
    resource = {'2': 22, '3': '', 'scheme': [{'name': 1, 'p1': ''}, {'name': 2}]}
    res = inheritDataClass(prnt_res, resource)
