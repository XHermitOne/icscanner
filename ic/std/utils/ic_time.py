#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций работы с временными даннами и датами.
"""

# --- Подключение библиотек ---
import wx
import time
import datetime
import calendar

from ic.std.log import log

_ = wx.GetTranslation

__version__ = (0, 0, 0, 2)

# --- Константы и переменные ---
DEFAULT_DATETIME_FMT = '%d.%m.%Y'
DEFAULT_DATE_FMT = '%Y.%m.%d'

# Формат хранения даты/времени в БД
DEFAULT_DATETIME_DB_FMT = '%Y.%m.%d %H:%M:%S'

DEFAULT_TIME_FMT = '%H:%M:%S'


# --- Функции работы с датой/временем ---
def getWeekList():
    """
    Список дней недели.
    """
    return [_('Monday'), _('Tuesday'), _('Wednesday'),
            _('Thursday'), _('Friday'),
            _('Saturday'), _('Sunday')]


def icTimeInRange(Range_, Time_):
    """
    Проверка попадает ли указанное время в указанный временной диапазон.
    @param Range_: Временной диапазон в формате кортежа 
        (нач-час,нач-мин,окон-час,окон-мин).
    @param Time_: Время в формате кортежа (час,мин).
    @return: Возвращает True, если время в диапазоне.
    """
    try:
        if Range_[0] < Time_[0] < Range_[2]:
            return True
        elif Time_[0] == Range_[0] or Time_[0] == Range_[2]:
            if Range_[1] < Time_[1] < Range_[3]:
                return True
        return False
    except:
        return None


def DateTime2StdFmt(DateTime_=None):
    """
    Представление времени в стандартном строковом формате.
    @param DateTime_: Время и дата, если None,  то текущие.
    """
    if DateTime_ is None:
        DateTime_ = time.time()
    return time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(DateTime_))


def TodayFmt(Fmt_=DEFAULT_DATETIME_FMT):
    """
    Сегодняшнее число в формате.
    @param Fmt_: Задание формата.
    @return: Возвращает строку или None в случае ошибки.
    """
    try:
        return datetime.date.today().strftime(Fmt_)
    except:
        log.fatal(u'Error in ic_time.TodayFmt')
        return None


def Today():
    """
    Сегодняшнее число в формате date.
    @return: Объект date или None в случае ошибки.
    """
    try:
        return datetime.date.today()
    except:
        log.fatal(u'ERROR in ic_time.Today')
        return None


def Now():
    """
    Сегодняшнее число/время.
    @return: <datetime>
    """
    return datetime.datetime.now()


def NowFmt(Fmt_='%d.%m.%Y %H:%M:%S'):
    """
    Сегодняшнее число/время в формате.
    @param Fmt_: Задание формата.
    @return: Возвращает строку или None в случае ошибки.
    """
    try:
        return time.strftime(Fmt_, time.localtime(time.time()))
    except:
        log.fatal(u'ERROR in ic_time.NowFmt')
        return None


def MaxDayFmt(Fmt_=DEFAULT_DATETIME_FMT):
    """
    Максимально возможная дата в формате.
    @param Fmt_: Задание формата.
    @return: Возвращает строку или None в случае ошибки.
    """
    try:
        return datetime.date(datetime.MAXYEAR, 12, 31).strftime(Fmt_)
    except:
        log.fatal(u'ERROR in ic_time.MaxDayFmt')
        return None


def MinDayFmt(Fmt_=DEFAULT_DATETIME_FMT):
    """
    Минимально возможная дата в формате.
    @param Fmt_: Задание формата.
    @return: Возвращает строку или None в случае ошибки.
    """
    try:
        return datetime.date(datetime.MINYEAR, 01, 01).strftime(Fmt_)
    except:
        log.fatal(u'ERROR in ic_time.MinDayFmt')
        return None


def DateTimeTuple(DateTimeStr_='01.01.2005', Fmt_=DEFAULT_DATETIME_FMT):
    """
    Представление даты_времени в виде кортежа.
    @param DateTimeStr_: Число в строковом формате.
    @param Fmt_: Формат представления строковы данных.
    @return: Представление даты_времени в виде кортежа.
    """
    try:
        return time.strptime(DateTimeStr_, Fmt_)
    except:
        log.fatal(u'ERROR in ic_time.DateTimeTuple')
        return None


def MonthDT(DateTimeStr_='01.01.2005', Fmt_=DEFAULT_DATETIME_FMT):
    """
    Месяц в формате datetime.
    @param DateTimeStr_: Число в строковом формате.
    @param Fmt_: Формат представления строковы данных.
    @return: Возвращает укзанный в строке месяц в формате datetime.
    """
    try:
        dt_tuple = DateTimeTuple(DateTimeStr_, Fmt_)
        return datetime.date(dt_tuple[0], dt_tuple[1], 1)
    except:
        log.fatal(u'ERROR in ic_time.MonthDT : %s' % dt_tuple)
        return None


def OneMonthDelta():
    """
    1 месяц в формате timedelta.
    """
    try:
        return datetime.timedelta(31)
    except:
        log.fatal(u'ERROR in ic_time.OneMonthDelta')
        return None


def setDayDT(DateTime_, Day_=1):
    """
    Установить первой дату объекта dete.
    """
    try:
        return datetime.date(DateTime_.year, DateTime_.month, Day_)
    except:
        log.fatal(u'ERROR in ic_time.setDayDT')
        return None


def convertDateTimeFmt(DateTimeStr_, OldFmt_=DEFAULT_DATETIME_FMT, NewFmt_=DEFAULT_DATETIME_FMT):
    """
    Преобразовать строковое представления даты-времени в другой формат.
    @param DateTimeStr_: Число в строковом формате.
    @param OldFmt_: Старый формат представления строковы данных.
    @param NewFmt_: Старый формат представления строковы данных.
    @return: Возвращает строку даты-времени в новом формате.
    """
    try:
        date_time_tuple = DateTimeTuple(DateTimeStr_, OldFmt_)
        return time.strftime(NewFmt_, date_time_tuple)
    except:
        log.fatal(u'ERROR in convertDateTimeFmt')
        return None


def strDateFmt2DateTime(DateStr_, Fmt_=DEFAULT_DATETIME_FMT):
    """
    Преобразование строкового представления даты в указанном формате
    в формат datetime.
    @return: Возвращает объект datetime или None в случае ошибки.
    """
    try:
        date_time_tuple = DateTimeTuple(DateStr_, Fmt_)
        year = date_time_tuple[0]
        month = date_time_tuple[1]
        day = date_time_tuple[2]
        return datetime.date(year, month, day)
    except:
        log.fatal(u'ERROR in strDateFmt2DateTime')
        return  None


def strDateTimeFmt2DateTime(DateTimeStr_, Fmt_=DEFAULT_DATETIME_FMT):
    """
    Преобразование строкового представления даты/времени в указанном формате
    в формат datetime.
    @return: Возвращает объект datetime или None в случае ошибки.
    """
    try:
        date_time_tuple = DateTimeTuple(DateTimeStr_, Fmt_)
        year = date_time_tuple[0]
        month = date_time_tuple[1]
        day = date_time_tuple[2]
        hour = date_time_tuple[3]
        minute = date_time_tuple[4]
        second = date_time_tuple[5]
        return datetime.datetime(year, month, day, hour, minute, second)
    except:
        log.fatal(u'ERROR in strDateTimeFmt2DateTime args: %s' % DateTimeStr_)
        return None


def getNowYear():
    """
    Текущий год.
    """
    return int(NowFmt('%Y'))


def getMonthDaysCount(Month_, Year_=None):
    """
    Определить сколько дней в месяце по номеру месяца.
    @param Month_: Номер месяца 1..12.
    @param Year_: Год. Если None, то текущий год.
    """
    if Year_ is None:
        Year_ = getNowYear()
    else:
        Year_ = int(Year_)
    month_days = 0
    calendar_list = calendar.Calendar().monthdayscalendar(Year_, Month_)
    for week in calendar_list:
        month_days += len([day for day in week if day != 0])
    return month_days


def getWeekDay(Day_, Month_, Year_=None):
    """
    Номер дня недели 1..7.
    @param Day_: День.
    @param Month_: Номер месяца 1..12.
    @param Year_: Год. Если None, то текущий год.
    """
    if Year_ is None:
        Year_ = getNowYear()
    return calendar.weekday(int(Year_), int(Month_), int(Day_))+1


def getWeekPeriod(nweek, year=None):
    """
    Возвращает период дат нужной недели.
    @return: Возващает картеж периода дат нужной недели. 
    """
    if not year:
        year = getNowYear()
        
    d1 = datetime.date(year, 1, 1)
    if d1.weekday() > 0:
        delt = datetime.timedelta(7 - d1.weekday())
    else:
        delt = datetime.timedelta(0)
        
    beg = d1 + datetime.timedelta((nweek-1)*7) + delt
    end = d1 + datetime.timedelta((nweek-1)*7+6) + delt
    return beg, end


def genUnicalTimeName():
    """
    Генерация уникальоного имени по текущему времени.
    """
    return NowFmt('%Y%m%d_%H%M%S')


def pydate2wxdate(date):
    """
    Преобразовать <datetime> тип в <wx.DateTime>.
    @param date: Дата <datetime>.
    @return: Дата <wx.DateTime>.
    """
    if date is None:
        return None

    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTimeFromDMY(*dmy)


def wxdate2pydate(date):
    """
    Преобразовать <wx.DateTime> тип в <datetime>.
    @param date: Дата <wx.DateTime>.
    @return: Дата <datetime>.
    """
    if date is None:
        return None

    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = list(map(int, date.FormatISODate().split('-')))
        return datetime.date(*ymd)
    else:
        return None


def pydatetime2wxdatetime(dt):
    """
    Преобразовать <datetime> тип в <wx.DateTime>.
    @param dt: Дата-время <datetime>.
    @return: Дата-время <wx.DateTime>.
    """
    if dt is None:
        return None

    assert isinstance(dt, (datetime.datetime, datetime.date))
    tt = dt.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    hms = (tt[2], tt[1]-1, tt[0])
    result = wx.DateTimeFromDMY(*dmy)
    result.SetHour(hms[0])
    result.SetMinute(hms[1])
    result.SetSecond(hms[2])
    return result


def wxdatetime2pydatetime(dt):
    """
    Преобразовать <wx.DateTime> тип в <datetime>.
    @param dt: Дата-время <wx.DateTime>.
    @return: Дата-время <datetime>.
    """
    if dt is None:
        return None

    assert isinstance(dt, wx.DateTime)
    if dt.IsValid():
        ymd = [int(t) for t in dt.FormatISODate().split('-')]
        hms = [int(t) for t in dt.FormatISOTime().split(':')]
        dt_args = ymd+hms
        return datetime.datetime(*dt_args)
    else:
        return None


def date2datetime(dt):
    """
    Конвертация datetime.date в datetime.datetime.
    @param dt: Дата в формате datetime.date
    @return: Дата в формате datetime.datetime
    """
    return datetime.datetime.combine(dt, datetime.datetime.min.time())


def test():
    """
    Тестирование функций.
    """
    pass


if __name__ == '__main__':
    test()
