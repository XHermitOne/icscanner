#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалоговых функций пользователя.
"""

import os
import os.path
import wx
import wx.animate
import thread
import time

__version__ = (0, 0, 1, 2)

# Задержка между кадрами
FRAME_DELAY = 0.3

ic_wait_process_dlg = None


def wait_func(parent, message,
              function, func_args=(), func_kwargs={},
              art_frames=None):
    """
    Окно ожидания.
    @param parent: Ссылка на окно.
    @param message: Текст диалога.
    @param function: Функция, которую необходимо подождать.
    @param func_args: Аргументы функции.
    @param func_kwargs: Именованные аргументы функции.
    @param art_frames: Файлы-кадры.
    """
    global ic_wait_process_dlg
    
    wait_result = [None]
    if not art_frames:
        # Определить кадры по умолчанию
        cur_dir = os.path.dirname(__file__)
        if not cur_dir:
            cur_dir = os.getcwd()
        wait_dir = os.path.join(cur_dir, 'img', 'wait')
        art_gif = os.path.join(wait_dir, 'spinner.gif')

    if parent is None:
        parent = wx.GetApp().GetTopWindow()
    ic_wait_process_dlg = wait_box = icWaitBox(parent, message, art_gif)
    wait_box.set_result_list(wait_result)

    # Запустить функцию ожидания
    thread.start_new(wait_box.run, (function, func_args, func_kwargs))
    wait_box.ShowModal()
    wait_box.Destroy()
    ic_wait_process_dlg = None
    return wait_result[0]


def wait_deco(f):
    def func(*arg, **kwarg):
        return wait_func(arg[0], u'Идет выполнение', f, arg, kwarg)
    return func


def wait_noparentdeco(f):
    def func(*arg, **kwarg):
        return wait_func(None, u'Идет выполнение', f, arg, kwarg)
    return func


def set_waitbox_label(label):
    if ic_wait_process_dlg:
        sx, sy = ic_wait_process_dlg.GetSize()
        ic_wait_process_dlg.SetSize((len(label)*10 + 20, sy))
        ic_wait_process_dlg.CenterOnScreen()
        ic_wait_process_dlg.set_label(label)
        

class icWaitBox(wx.Dialog):
    def __init__(self, parent, message, art, style=0):
        """
        Конструктор.
        """
        if parent is None:
            style = wx.STAY_ON_TOP
            
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, size=wx.Size(200, 34), style=style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        self.msg = wx.StaticText(self, -1, message)
        self._lastTime = time.clock()

        self.ani = wx.animate.Animation(art)
        self.ani_ctrl = wx.animate.AnimationCtrl(self, -1, self.ani)
        self.ani_ctrl.SetUseWindowBackgroundColour()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.ani_ctrl, 0, wx.CENTRE, 5)
        sizer.Add(self.msg, 0, wx.CENTRE, 5)

        self.ani_ctrl.Play()

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.CenterOnScreen()

        self._running = True    # Признак запущенной функции
        self._closed = False    # Признак закрытия окна
        self._result_list = None
        
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_close)

    def refresh(self):
        """
        """
        evt = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(evt)

    def set_result_list(self, result_list):
        self._result_list = result_list
        
    def on_check_close(self, event=None):
        """
        Проверка закрытия окна.
        """
        if not self._running and not self._closed:
            try:
                self.EndModal(wx.ID_OK)
            except:
                pass
            self._closed = True
            
        if event:
            event.Skip()
        
    def run(self, function, args, kwargs):
        """
        Запуск ожидания функции.
        """
        self._running = True
        result = function(*args, **kwargs)
        self._running = False
        # Сбросить в результирующий список
        if isinstance(self._result_list, list):
            self._result_list[0] = result
            
    def set_label(self, label=None):
        """
        """
        if self.msg:
            self.refresh()
            if label:
                self.msg.SetLabel(label)
            evt = wx.PaintEvent(self.msg.GetId())
            self.msg.GetEventHandler().ProcessEvent(evt)


def test():
    def funcA():
        time.sleep(5)

    app = wx.PySimpleApp()
    result = wait_func(None, u'Ожидание длинное  ', funcA)
    app.MainLoop()
    print((u'Result: %s' % result))

if __name__ == '__main__':
    test()
