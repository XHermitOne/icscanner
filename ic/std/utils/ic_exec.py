#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций выполнения запросов и методов пользователя.

@var SELF_DOT_TAG: Символ, определяющий в методе кода ссылку на объект,
    который вызывает этот метод.
@var CODE_UNIT_TAG: Если строка начинается с этого символа ('@'), 
    то это выполняемая функция (блок кода).
"""

# --- Подключение библиотек ---

import wx
from types import *
import os
from ic.log import log

import ic.utils.util
import ic.utils.resource
from . import ic_util
from . import ic_file
from ic.kernel import io_prnt

_ = wx.GetTranslation

# --- Основные константы ---
RES_MODULE = 'module'   # <модуль,  в котором находится функция, строка>
RES_METHOD = 'method'   # <функция, блок кода>

SELF_DOT_TAG = '_.'
SELF_TAG = '#'
CODE_UNIT_TAG = '@'

# --- Спецификации ---
# Спецификация словаря функции
SPC_IC_EXEC = {
                RES_MODULE: '',     # <модуль,  в котором находится функция, строка>
                RES_METHOD: '@',    # <функция, блок кода>
              }

# Спецификация функции системы
SPC_IC_FUNC = {
               'name': 'func1',     # < код-имя функции, строка>,
               'type': 'icFunc',    # <тип 'icFunc', строка>,
               'description': '',   # <описание, строка>,
               'import': {},        # <словарь, описывающий импортируемые имена для вычисления выражений>,
               'func': '@',         # <сама функция, строка>,
               'len': -1,           # <длина возвращаемого значения, целое>,
               'mask': '',          # <шаблон возвращаемого значения, регулярное выражение>,
               'date': None,        # <дата последнего изменения, строка>,
              }


def ExecuteMethod(Func_, self=None):
    """
    Выполнить метод.
    @param self: ссылка на объект, который вызывает эту функцию.
    @param Func_: словарь функции (см. документацию на ресурсные файлы).
    """
    try:
        if self is not None:
            try:
                name_space = self.GetContext()
            except:
                name_space = ic.utils.util.InitEvalSpace(locals())
        else:
            name_space = ic.utils.util.InitEvalSpace(locals())
        name_space['self'] = self
        
        ret = ic.utils.util.ic_eval(Func_, evalSpace=name_space)
        
        if ret[0]:
            return ret[1]
        else:
            return None
    except:
        io_prnt.outErr(_('Execute method error: %s') % (str(Func_)))
        return None


def ExecuteCode(Code_, self=None):
    """
    Выполнить блок кода.
    @param self: ссылка на объект, который вызывает эту функцию.
    @param Code_: строка функции.
        Если строка начинается с символа '@', то это выполняемая функция.
    """
    try:
        # Проверка аргументов
        if type(Code_) <> StringType:
            return Code_
        elif Code_[0] <> CODE_UNIT_TAG:
            return Code_
        # Убрать признак блока кода
        Code_ = Code_[1:]
        # Перед выполнением метода заменить тег, определяющий объект,
        # который вызвал эту функцию, на self
        if self <> None:
            Code_ = Code_.replace(SELF_DOT_TAG, 'self.')
        # Выполнить
        return ic_util.icEval(Code_, 0, locals(), globals())
    except:
        io_prnt.outErr()


def IsEmptyMethod(Func_):
    """
    Проверка пустой словарь функции или нет.
    @param Func_: Словарь функции.
    @return: Истина - если словарь пустой (ни модуль, ни метод не определены).
             В противном случае - ложь.
    """
    try:
        find = True
        if (not Func_) or Func_ == 'None':
            return True

        # Проверка модуля
        if (RES_MODULE in Func_) == 1 and Func_[RES_MODULE]:
            find = False
        else:
            # Проверка метода
            if (RES_METHOD in Func_) == 1 and Func_[RES_METHOD] <> '' and \
                    Func_[RES_METHOD] <> '@' and Func_[RES_METHOD] <> None:
                find = False
        return find
    except:
        io_prnt.outErr('Function: %s' % str(Func_))


def GetNameFuncFromCode(Code_):
    """
    Получить имя функции из блока кода.
    @param Code_: Блок кода.
        Блок кода - строка в формате:
            @ИмяФункции(аргументы)
    """
    try:
        # Убрали @
        name_func = Code_[1:]
        i_find = name_func.find('(')
        # Если это константа, тогда вернуть ее имя
        if i_find == -1:
            return name_func
        return name_func[:i_find]
    except:
        return ''


def icSysCmd(sCommand):
    """
    Функция выполняет комманду системы.
    @param sCommand: Строка системной команды.
    """
    log.debug(u'Выполнение команды: <%s>' % sCommand)
    return os.system(sCommand)


def icExecFunc(Func_):
    """
    Выполнить функцию и возвратить значение.
    @param Func_: Описание функции (См. спецификацию SPC_IC_FUNC).
    @return: Возвращает значение,  которое возвращает функция.
    """
    try:
        name_space = ic.utils.util.ic_import(Func_['import'])
        return ic.utils.util.ic_eval(Func_['func'], -1, name_space)
    except:
        io_prnt.outErr()
        return None


def icExecFuncByName(FuncName_, Funcs_):
    """
    Выполнить функцию и возвратить значение по его имени.
    @param FuncName_: Имя функции (См. fnc_fmt.doc).
    @param Funcs_: Описание функций (См. fnc_fmt.doc) или 
        имя файла где оно храниться.
    @return: Возвращает значение,  которое возвращает функция.
    """
    try:
        if type(Funcs_) == StringType:
            Funcs_ = ic_res.ReadAndEvalFile(Funcs_)
        return icExecFunc(Funcs_[FuncName_])
    except:
        io_prnt.outErr()
        return None


def icMethod(MethodStr_, NameSpace_=None):
    """
    Вызов метода.
    @param MethodStr_: Строковый вызов метода. Например 'NSI.method1(a1=3,s2=4)'.
    @param NameSpace_: Пространство имен.
    """
    try:
        # Сначала разобрать строку
        method_name = MethodStr_.split('{')[0]
        if NameSpace_ is None:
            NameSpace_ = locals()
        method_args_str = MethodStr_[len(method_name):]
        method_args = {}
        if method_args_str:
            method_args = eval(method_args_str, NameSpace_)

        sub_sys = None
        if method_name.find('.') <> -1:
            method_name_split = method_name.split('.')
            sub_sys = method_name_split[0]
            method_name = method_name_split[1]

        value = ic.utils.resource.method(method_name, sub_sys, NameSpace_, **method_args)
        return value
    except:
        io_prnt.outErr(_('Execute method error: %s') % MethodStr_)
        return None

_run_py_code = '''import sys
import ic.engine.main
from os.path import dirname, abspath

if not sys.argv[1:]:
    path = dirname(abspath(__file__)).replace("\\\\",'/') 
    main_sys = path.split('/')[-1]
    args = ['-run', '-dbg', '%s/%s/' % (path, main_sys), '-s']
    ic.engine.main.main(args)
else:
    ic.engine.main.run()
'''


def CreateRunApp(PrjDir_):
    """
    Создать если надо модуль запуска прикладной системы.
    @return: True/False.
    """
    run_py_file_name = ic_file.AbsolutePath(PrjDir_)+'/run.py'
    
    if not ic_file.Exists(run_py_file_name):
        run_py_file = None
        try:
            run_py_file = open(run_py_file_name, 'wt')
            run_py_file.write(_run_py_code)
            run_py_file.close()
            return True
        except:
            if run_py_file:
                run_py_file.close()
            raise
    return False
        
    
def RunTask(Cmd_):
    """
    Запуск комманды, как отдельной задачи.
    @type Cmd_: C{string}
    @param Cmd_: Комманда системы.
    """
    if ic_util.isOSWindowsPlatform():
        return RunTaskBAT(Cmd_)
    return RunTaskSH(Cmd_)


def RunTaskSH(Cmd_):
    """
    Запуск комманды, как отдельной задачи с отдельной консолью в Linux.
    @type Cmd_: C{string}
    @param Cmd_: Комманда системы.
    """
    run_sh_name = ic_file.AbsolutePath('./run.sh')
    if ic_file.IsFile(run_sh_name):
        ic_file.Remove(run_sh_name)
    f = None
    try:
        f = open(run_sh_name, 'w')
        f.write(Cmd_)
        f.close()
        f = None
        # Запуск исполняемого скрипта
        io_prnt.outLog(_('Run task: %s') % run_sh_name)
        os.system('gnome-terminal --command \'sh %s\'' % run_sh_name)
    except:
        io_prnt.outErr(_('Run task error: %s') % run_sh_name)
        if f:
            f.close()


def RunTaskBAT(Cmd_):
    """
    Запуск комманды, как отдельной задачи с отдельной консолью.
    @type Cmd_: C{string}
    @param Cmd_: Комманда системы.
    """
    run_bat_name = ic_file.AbsolutePath('./run.bat')
    if ic_file.IsFile(run_bat_name):
        ic_file.Remove(run_bat_name)
    f = None
    try:
        f = open(run_bat_name, 'w')
        f.write(Cmd_)
        f.close()
        f = None
        # Запуск батника
        io_prnt.outLog(_('Run task: %s') % run_bat_name)
        os.startfile(run_bat_name)
    except:
        io_prnt.outErr(_('Run task error: %s') % run_bat_name)
        if f:
            f.close()


def RunProgramm(Cmd_, Mode_=os.P_NOWAIT):
    """
    Запуск программы на выполнение.
    @type Cmd_: C{string}
    @param Cmd_: Комманда системы.
    @param Mode_: Режим выполнения комманды. См os режимы выполнения.
    @return: True/False.
    """
    try:
        parse_args = Cmd_.strip().split(' ')
        args = []
        i = 0
        while i < len(parse_args):
            parse_arg = parse_args[i]
            if parse_arg[0] == '"' and parse_arg[-1] <> '"':
                while parse_arg[-1] <> '"' and i < len(parse_args):
                    i += 1
                    parse_arg += ' '+parse_args[i]
            # Стереть """
            if parse_arg[0] == '"':
                parse_arg = parse_arg[1:]
            if parse_arg[-1] == '"':
                parse_arg = parse_arg[:-1]
                        
            args.append(parse_arg)
            i += 1
        io_prnt.outLog('RunProgramm: %s' % args)
        os.spawnve(Mode_, args[0], args, os.environ)
        return True
    except:
        io_prnt.outErr(_('Run programm error: %s') % Cmd_)
        return False


def RunOSCommand(Cmd_, Wait_=True):
    """
    Запуск комманды OC.
    @type Cmd_: C{string}
    @param Cmd_: Комманда системы.
    @param Wait_: Команда ожидания процесса.
    @return: True/False.
    """
    try:
        if Wait_:
            os.system(Cmd_)
        else:
            # Если ожидание выключено, то скорее всего это программа
            return RunProgramm(Cmd_)
        return True
    except:
        io_prnt.outErr(_('Command error: %s') % Cmd_)
        return False


def execFuncStr(FuncStr_, NameSpace_=None, ReImport_=False, *args, **kwargs):
    """
    Выполнение строковой функции в формате: пакеты.модуль.функция(аргументы).
    @type FuncStr_: C{string}
    @param FuncStr_: Строковая функция.
    @type NameSpace_: C{dictionary}
    @param NameSpace_: Пространство имен.
    @type ReImport_: C{bool}
    @param ReImport_: Переимпортировать модуль функции?
    @return: Вовращает результат выполнения функции или None  в случае ошибки.
    """
    result = None
    try:
        # Выделить модуль функции
        func_import = FuncStr_.split('(')[0].split('.')
        func_mod = '.'.join(func_import[:-1])
        # Подготовить пространство имен
        if NameSpace_ is None or type(NameSpace_) <> type({}):
            NameSpace_ = {}

        # Выполнение функции
        try:
            try:
                if ReImport_:
                    ic.utils.util.icUnLoadSource(func_mod)
                import_str = 'import '+func_mod
                exec import_str
            except:
                io_prnt.outErr(_('Import module error: %s') % import_str)
            NameSpace_.update(locals())
            result = eval(FuncStr_, globals(), NameSpace_)
        except:
            io_prnt.outErr(_('Run module error: %s') % (FuncStr_, func_mod))
    except:
        io_prnt.outErr(_('Error in function ic_exec.execFuncStr, %s') % FuncStr_)
    
    return result
