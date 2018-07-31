#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль сервисных функций программиста
"""

# --- Подключение библиотек ---
import sys
import os
import os.path
import inspect
import wx

from encodings.aliases import aliases

from ic.std.log import log
try:
    import win32api
    import win32con
    import regutil
except ImportError:
    log.error(u'ImportError: PyWin32')

try:
    import DevId
except:
    log.error(u'ImportError: Recompiled DevId module')

__version__ = (0, 0, 1, 2)


# --- Функции ---
def IsSubClass(Class1_, Class2_):
    """
    Функция определяет является ли Class1_ базовым для Class2_. Проверка
    производится рекурсивно.
    @param Class1_: Объект класса.
    @param Class2_: Объект класса.
    @return: Возвращает результат отношения (1/0).
    """
    return issubclass(Class2_, Class1_)


def SpcDefStruct(spc, struct):
    """
    Дополняет структуру описания объекта до требований спецификации.
    @type spc: C{dictionary}.
    @param spc: Словарь описания спецификации.
    @type struct: C{dictionary}.
    @param struct: Словарь описания структуры.
    @rtype: C{dictionary}.
    @return: Дополненная структура.
    """
    try:
        def_struct = icSpcDefStruct(spc, struct)
        # Коррекция типов
        for name, value in def_struct.items():
            if name in spc and isinstance(def_struct['name'], str) and not isinstance(spc['name'], str):
                try:
                    # Возможно это не строка
                    def_value = eval(value)
                except:
                    # Нет наверно это строка
                    def_value = value
                def_struct[name] = def_value
        return def_struct
    except:
        return struct


def getAttrValue(AttrName_, SPC_):
    """
    Получить нормированное значение свойства из спецификации.
    @param AttrName_: Имя атрибута.
    @param SPC_: Спецификация.
    """
    try:
        # Нормализация по типам
        if isinstance(SPC_[AttrName_], str):
            try:
                # Возможно это не строка
                value = eval(SPC_[AttrName_])
            except:
                # Нет это все таки строка
                value = SPC_[AttrName_]
            SPC_[AttrName_] = value
        return SPC_[AttrName_]
    except:
        log.fatal()
        return None


def getStrInQuotes(Value_):
    """
    Если Value_ - строка то обрамляет ее одинарными кавычками, если нет,
    то просто преабразует в строку.
    """
    if isinstance(Value_, str):
        return '\'%s\'' % Value_
    elif isinstance(Value_, unicode):
        return u'\'%s\'' % Value_
    else:
        return str(Value_)


def KeyToText(Key_, Shift_=0, Alt_=0, Ctrl_=0):
    """
    Функция преабразует код клавиши в текстовый эквивалент.
    @param Key_: код клавиши.
    @param Shift_: флаг клавиши Shift.
    @param Alt_: флаг клавиши Alt.
    @param Ctrl_: флаг клавиши Ctrl.
    @return: Возвращает текстовую строку, например 'Alt+X'.
    """
    result = ''
    if Shift_ == 1:
        result += 'Shift+'
    if Alt_ == 1:
        result += 'Alt+'
    if Ctrl_ == 1:
        result += 'Ctrl+'
    if Key_ == wx.WXK_RETURN:
        result += 'Enter'
    elif Key_ == wx.WXK_ESCAPE:
        result += 'Esc'
    elif Key_ == wx.WXK_DELETE:
        result += 'Del'
    elif Key_ == wx.WXK_TAB:
        result += 'Tab'
    elif Key_ == wx.WXK_SPACE:
        result += 'Space'
    elif Key_ == wx.WXK_END:
        result += 'End'
    elif Key_ == wx.WXK_HOME:
        result += 'Home'
    elif Key_ == wx.WXK_PAUSE:
        result += 'Pause'
    elif Key_ == wx.WXK_LEFT:
        result += 'Left'
    elif Key_ == wx.WXK_UP:
        result += 'Up'
    elif Key_ == wx.WXK_RIGHT:
        result += 'Right'
    elif Key_ == wx.WXK_DOWN:
        result += 'Down'
    elif Key_ == wx.WXK_INSERT:
        result += 'Ins'
    elif Key_ == wx.WXK_F1:
        result += 'F1'
    elif Key_ == wx.WXK_F2:
        result += 'F2'
    elif Key_ == wx.WXK_F3:
        result += 'F3'
    elif Key_ == wx.WXK_F4:
        result += 'F4'
    elif Key_ == wx.WXK_F5:
        result += 'F5'
    elif Key_ == wx.WXK_F6:
        result += 'F6'
    elif Key_ == wx.WXK_F7:
        result += 'F7'
    elif Key_ == wx.WXK_F8:
        result += 'F8'
    elif Key_ == wx.WXK_F9:
        result += 'F9'
    elif Key_ == wx.WXK_F10:
        result += 'F10'
    elif Key_ == wx.WXK_F11:
        result += 'F11'
    elif Key_ == wx.WXK_F12:
        result += 'F12'
    elif Key_ == wx.WXK_F13:
        result += 'F13'
    elif Key_ == wx.WXK_F14:
        result += 'F14'
    elif Key_ == wx.WXK_F15:
        result += 'F15'
    elif Key_ == wx.WXK_F16:
        result += 'F16'
    elif Key_ == wx.WXK_F17:
        result += 'F17'
    elif Key_ == wx.WXK_F18:
        result += 'F18'
    elif Key_ == wx.WXK_F19:
        result += 'F19'
    elif Key_ == wx.WXK_F20:
        result += 'F20'
    elif Key_ == wx.WXK_F21:
        result += 'F21'
    elif Key_ == wx.WXK_F22:
        result += 'F22'
    elif Key_ == wx.WXK_F23:
        result += 'F23'
    elif Key_ == wx.WXK_F24:
        result += 'F24'
    else:
        if Key_ < 256:
            result += chr(Key_)
            
    return result

# Наполнитель позиций при отображении вложенности пунктов в компоненте списка
PADDING = '    '


def StructToTxt(Struct_, Level_=0):
    """
    Перевод словарно-списковой структуры в форматированный текст.
    @param Struct_ : словарно-списковая структура.
    @param Level_: уровень вложенности (д.б. 0).
    """
    try:
        txt = ''
        obj_type = type(Struct_)
        if obj_type == list:
            txt = txt+'\n'+Level_*PADDING+'[\n'
            for obj in Struct_:
                txt += Level_*PADDING
                txt += StructToTxt(obj, Level_+1)
                txt += ',\n'
            if len(Struct_) != 0:
                txt = txt[:-2]
            txt = txt+'\n'+Level_*PADDING+']'
        elif obj_type == dict:
            txt = txt+'\n'+Level_*PADDING+'{\n'
            keys = Struct_.keys()
            values = Struct_.values()
            for key in keys:
                txt = txt+Level_*PADDING+'\''+key+'\':'
                txt += StructToTxt(Struct_[key], Level_+1)
                txt += ',\n'
            if len(keys) != 0:
                txt = txt[:-2]
            txt = txt+'\n'+Level_*PADDING+'}'
        elif obj_type == str:
            # Появляется косяк с разделителем папок в именах путей
            # Проверка на кавычки
            txt = txt+'\''+Struct_.replace('\'',
                                           '\\\'').replace('\'',
                                                           '\\\'').replace('\r',
                                                                           '\\r').replace('\n',
                                                                                          '\\n').replace('\t',
                                                                                                         '\\t')+'\''
        elif obj_type == unicode:
            # Появляется косяк с разделителем папок в именах путей
            # Проверка на кавычки
            txt = txt+'u\''+Struct_.replace('\'',
                                            '\\\'').replace('\'',
                                                            '\\\'').replace('\r',
                                                                            '\\r').replace('\n',
                                                                                           '\\n').replace('\t',
                                                                                                          '\\t')+'\''
        else:
            txt += str(Struct_)

        # Убрать первый перевод каретки
        if txt[0] == '\n' and (not Level_):
            txt = txt[1:]
        return txt
    except:
        log.fatal(u'Ошибка %d' % Level_)


def DelKeyInDictTree(Dict_, Key_):
    """
    Функция удаляет из словаря рекурсивно все указанные ключи.
    @param Dict_: Непосредственно словарь или список.
    @param Key_: Ключ, который необходимо удалить.
    """
    # Если это у нас словарь, то ...
    if type(Dict_) is dict:
        try:
            # Сначала удаляем ключ на этом уровне.
            del Dict_[Key_]
        except:
            pass
        # Затем спускаемся на уровень ниже и обрабатываем
        for item in Dict_.values():
            DelKeyInDictTree(item, Key_)
    # а если список, то перебираем элементы
    elif type(Dict_) is list:
        for item in Dict_:
            DelKeyInDictTree(item, Key_)
    # а если не то и не другое, то ничего с ним не делать
    else:
        return


def SetKeyInDictTree(Dict_, Key_, Value_):
    """
    Функция устанавливает значенеи ключа в словаре рекурсивно.
    @param Dict_: Непосредственно словарь или список.
    @param Key_: Ключ, который необходимо установить.
    @param Value_: Значение ключа.
    """
    # Если это у нас словарь, то ...
    if type(Dict_) is dict:
        try:
            # Сначала устанавливаем ключ на этом уровне.
            Dict_[Key_] = Value_
        except:
            pass
        # Затем спускаемся на уровень ниже и обрабатываем
        for item in Dict_.values():
            SetKeyInDictTree(item, Key_, Value_)
    # а если список, то перебираем элементы
    elif type(Dict_) is list:
        for item in Dict_:
            SetKeyInDictTree(item, Key_, Value_)
    # а если не то и не другое, то ничего с ним не делать
    else:
        return


def icEval(Code_, LogType_=-1, LocalSpace_=None, GlobalSpace_=None, Msg_=''):
    """
    Функция выполняет предобработку вычисляемого выражения, вычисляет с
    использование стандартной, функции eval(...), а также обрабатывает исключения. 
    В качестве локального пространства имен используется словарь LocalSpace. 
    В качестве глобального пространства имен берется словарь GlobalSpace.
    @type Code_: C{string}
    @param Code_: Вычисляемое выражение.
    @type LogType_: C{int}
    @param LogType_: Тип лога (0 - консоль, 1- файл, 2- окно лога)
    @param LocalSpace_: Пространство имен, необходимых для вычисления выражения
    @type LocalSpace: C{dictionary}
    @param GlobalSpace_: Глобальное пространство имен.
    @type GlobalSpace: C{dictionary}
    """
    if LocalSpace_ is None:
        LocalSpace_ = {}

    ret_val = ic_eval(Code_, LogType_, LocalSpace_, Msg_, GlobalSpace_)
    # Проверка правильно ли выполнена операция
    if ret_val[0] == 1:
        return ret_val[1]
    return None


def icObjToGlob(ObjName_, Obj_):
    """
    Поместить объект в глобальное пространство имен.
    @param ObjName_: Имя объекта в глобальном пространстве имен.
    @param Obj_: Сам объект.
    """
    try:
        globals()[ObjName_] = Obj_
        return True
    except:
        return False


def icFilesToGlob(*args):
    """
    Поместить структуры, хранящиеся в файлах в глобальное пространство имен.
    @param args: Имена файлов и имена структур в глобальном пространстве состояний
        передаются в формате:
            (ИмяСтруктуры1,ИмяФайла1),(ИмяСтруктуры2,ИмяФайла2),...
    """
    try:
        for cur_arg in args:
            if os.path.isfile(cur_arg[1]):
                tmp_buff = ic_res.ReadAndEvalFile(cur_arg[1])
                icObjToGlob(cur_arg[0], tmp_buff)
            else:
                log.warning(u'Не найден файл %s' % cur_arg[1])
        return True
    except:
        return False


def ReCodeString(String_, StringCP_, NewCP_):
    """
    Перекодировать из одной кодировки в другую.
    @param String_: Строка.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    """
    if NewCP_.upper() == 'UNICODE':
        # Кодировка в юникоде.
        if isinstance(String_, str):
            return unicode(String_, StringCP_)
        else:
            return String_

    if NewCP_.upper() == 'OCT' or NewCP_.upper() == 'HEX':
        # Закодировать строку в восьмеричном/шестнадцатеричном виде.
        return icOctHexString(String_, NewCP_)

    string = u''
    if isinstance(String_, str):
        if StringCP_.upper() != 'UNICODE':
            string = unicode(String_, StringCP_)
        else:
            string = unicode(String_)
        
    elif isinstance(String_, unicode):
        string = String_
        
    return string.encode(NewCP_)


def icOctHexString(String_, Code_):
    """
    Закодировать строку в восьмеричном/шестнадцатеричном виде.
    Символы с кодом < 128 не кодируются.
    @param String_:
    @param Code_: Кодировка 'OCT'-восьмеричное представление.
                            'HEX'-шестнадцатеричное представление.
    @return: Возвращает закодированную строку.
    """
    try:
        if Code_.upper() == 'OCT':
            fmt = '\\%o'
        elif Code_.upper() == 'HEX':
            fmt = '\\x%x'
        else:
            # Ошибка аргументов
            log.warning(u'Argument error in icOctHexString.')
            return None
        # Перебор строки по символам
        ret_str = ''
        for char in String_:
            code_char = ord(char)
            # Символы с кодом < 128 не кодируются.
            if code_char > 128:
                ret_str += fmt % code_char
            else:
                ret_str += char
        return ret_str
    except:
        log.fatal()
        return None


def icListStrRecode(List_, StringCP_, NewCP_):
    """
    Перекодировать все строки в списке рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param List_: Сам список.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный список.
    """
    lst = []
    # Перебор всех элементов списка
    for i in range(len(List_)):
        if isinstance(List_[i], list):
            # Элемент - список
            value = icListStrRecode(List_[i], StringCP_, NewCP_)
        elif isinstance(List_[i], dict):
            # Элемент списка - словарь
            value = icDictStrRecode(List_[i], StringCP_, NewCP_)
        elif isinstance(List_[i], tuple):
            # Элемент списка - кортеж
            value = icTupleStrRecode(List_[i], StringCP_, NewCP_)
        elif isinstance(List_[i], str) or isinstance(List_[i], unicode):
            value = ReCodeString(List_[i], StringCP_, NewCP_)
        else:
            value = List_[i]
        lst.append(value)
    return lst


def _isRUSString(String_):
    """
    Строка с рускими буквами?
    """
    if isinstance(String_, str):
        rus_chr = [c for c in String_ if ord(c) > 128]
        return bool(rus_chr)
    return False


def icDictStrRecode(Dict_, StringCP_, NewCP_):
    """
    Перекодировать все строки в словаре рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param Dict_: Сам словарь.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный словарь.
    """
    keys_ = Dict_.keys()
    # Перебор всех ключей словаря
    for cur_key in keys_:
        value = Dict_[cur_key]
        # Нужно ключи конвертировать?
        if _isRUSString(cur_key):
            new_key = ReCodeString(cur_key, StringCP_, NewCP_)
            del Dict_[cur_key]
        else:
            new_key = cur_key
            
        if isinstance(value, list):
            # Элемент - список
            Dict_[new_key] = icListStrRecode(value, StringCP_, NewCP_)
        elif isinstance(value, dict):
            # Элемент - cловарь
            Dict_[new_key] = icDictStrRecode(value, StringCP_, NewCP_)
        elif isinstance(value, tuple):
            # Элемент - кортеж
            Dict_[new_key] = icTupleStrRecode(value, StringCP_, NewCP_)
        elif isinstance(value, str) or isinstance(value, unicode):
            Dict_[new_key] = ReCodeString(value, StringCP_, NewCP_)

    return Dict_


def icTupleStrRecode(Tuple_, StringCP_, NewCP_):
    """
    Перекодировать все строки в кортеже рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param Tuple_: Сам кортеж.
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный кортеж.
    """
    # Перевести кортеж в список
    lst = list(Tuple_)
    # и обработать как список
    list_ = icListStrRecode(lst, StringCP_, NewCP_)
    # Обратно перекодировать
    return tuple(list_)


def icStructStrRecode(Struct_, StringCP_, NewCP_):
    """
    Перекодировать все строки в структуре рекурсивно в другую кодировку.
    @param Struct_: Сруктура (список, словарь, кортеж).
    @param StringCP_: Кодовая страница строки.
    @param NewCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованную структру.
    """
    if isinstance(Struct_, list):
        # Список
        struct = icListStrRecode(Struct_, StringCP_, NewCP_)
    elif isinstance(Struct_, dict):
        # Словарь
        struct = icDictStrRecode(Struct_, StringCP_, NewCP_)
    elif isinstance(Struct_, tuple):
        # Кортеж
        struct = icTupleStrRecode(Struct_, StringCP_, NewCP_)
    elif isinstance(Struct_, str) or isinstance(Struct_, unicode):
        #Строка
        struct = ReCodeString(Struct_, StringCP_, NewCP_)
    else:
        # Тип не определен
        struct = Struct_
    return struct


def icList2Str(List_, DivChar_):
    """
    Конвертация списка в строку с разделением символом разделителя.
    @param List_: Список.
    @param DivChar_: Символ разделителя
    @return: Возвращает сформированную строку.
    """
    ret_str = ''
    for cur_element in List_:
        ret_str += str(cur_element)
        # Если элемент не последний, то добавить символ разделителя
        if cur_element != List_[-1]:
            ret_str += DivChar_
    return ret_str


def GetHDDSerialNo():
    """
    Определить серийный номер HDD.
    """
    try:
        hdd_info = DevId.GetHDDInfo()
        return hdd_info[2]
    except:
        # Ошибка определения серийного номера HDD.
        log.fatal(u'Define HDD serial number error.')
        return ''


def GetRegValue(RegKey_, RegValue_=None):
    """
    Взять информацию из реестра относительно данного проекта.
    @param RegKey_: Ключ реестра.
    @param RegValue_: Имя значения из реестра.
    """
    hkey = None
    try:
        hkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, RegKey_)
        value = win32api.RegQueryValueEx(hkey, RegValue_)
        win32api.RegCloseKey(hkey)
        return value[0]
    except:
        if hkey:
            win32api.RegCloseKey(hkey)
        # Ошибка определения информации из реестра.
        log.fatal()
        return None


def findChildResByName(ChildrenRes_, ChildName_):
    """
    Поиск ресурсного описания дочернего объекта по имени.
    @param ChildrenRes_: Список ресурсов-описаний дечерних объектов.
    @return ChildName_: Имя искомого дочернего объекта.
    @return: Индекс ресурсного описания в списке, если 
        описания с таким именем не найдено, то возвращается -1.
    """
    try:
        return map(lambda child: child['name'], ChildrenRes_).index(ChildName_)
    except ValueError:
        return -1


def getFuncListInModule(ModuleObj_=None):
    """
    Получить список имен функций в модуле.
    @param ModuleObj_: Объект модуля. 
        Для использования модуль д.б. импортирован.
    @return: Возвращает список кортежей:
        [(имя функции, описание функции, объект функции),...]
    """
    if ModuleObj_:
        return [(func_name, ModuleObj_.__dict__[func_name].__doc__,
                                      ModuleObj_.__dict__[func_name]) for func_name in [f_name for f_name in ModuleObj_.__dict__.keys() if inspect.isfunction(ModuleObj_.__dict__[f_name])]]
    return None


def isOSWindowsPlatform():
    """
    Функция определения ОС.
    @return: True-если ОС-Windows и False во всех остальных случаях.
    """
    return bool(sys.platform[:3].lower() == 'win')


def get_encodings_list():
    """
    Список возможных кодировок.
    """
    try:
        result = reduce(lambda lst, code: lst if code in lst else lst+[code],
                        aliases.values(), [])
        result.sort()
        return result
    except:
        return ['UTF-8', 'UTF-16', 'CP1251', 'CP866', 'KOI8-R']


def encode_unicode_struct(Struct_, CP_='utf-8'):
    """
    Перекодировать все строки unicode структуры в  указанную кодировку.
    """
    return icStructStrRecode(Struct_, 'UNICODE', CP_)
