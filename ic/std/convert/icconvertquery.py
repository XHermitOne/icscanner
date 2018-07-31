#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print('import',__file__)

"""
Классы драйверов конвертера данных в табличное представление.
"""

#--- Подключение библиотек ---
#from ic.interfaces import icconvertdriverinterface
#from ic.db import tabclass
#from ic.db import ic_sqlobjtab
from ic.db import icsqlalchemy

from ic.utils import util

from ic.components.user import ic_tab_wrp
from ic.components.user import ic_field_wrp

from ic.engine import ic_user

#--- Спецификации ---
CONVERTQUERY_TYPE='ConvertQuery'

SPC_IC_CONVERTQUERY={
    'name':'default',
    'type':CONVERTQUERY_TYPE,
    'driver':None, #Драйвер доступа к данным
    'auto_clear':True, #Автоматическое очищение результирующей таблицы
    '__parent__':icsqlalchemy.SPC_IC_TABLE,
    }
    
CONVERTFIELD_TYPE='ConvertField'

SPC_IC_CONVERTFIELD={
    'name':'default',
    'type':CONVERTFIELD_TYPE,
    'driver':None, #Драйвер доступа к данным
    'src_name':None, #Имя источника данных, идентифицирующего значения поля
    '__parent__':icsqlalchemy.SPC_IC_FIELD,
    }

#--- Классы ---
class icConvertQueryPrototype:
    """
    Класс конвертера данных в табличное представление.
    """
    def __init__(self,component_spc=None):
        """
        Конструктор.
        """
        self.resource=component_spc

        #Объект управления проектом.
        self._prj_res_ctrl=None
        #Результирующая таблица
        self._tab=None
        
    def getName(self):
        """
        Имя объекта.
        """
        return self.resource['name']
        
    def getTableName(self):
        """
        Имя результирующей таблицы.
        """
        return self.resource['table']

    def getDBName(self):
        """
        Имя источника данных/БД результирующей таблицы.
        """
        return self.resource['source']
        
    def getDriverName(self):
        """
        Имя драйвера источника данных.
        """
        return self.resource['driver']
        
    def getAutoClear(self):
        """
        Автоматическое очищение результирующей таблицы.
        """
        return self.resource['auto_clear']
        
    def _isTableRes(self,TableResName_=None):
        """
        Проверить есть ли ресурсное описание результирующей таблицы.
        @param TableResName_: Имя ресурсного описание результирующей таблицы.
        Если None, тогда имя берется из ресурсного описания этого компонента.
        """
        if TableResName_ is None:
            TableResName_=self.getTableName()
            
        #Открыть проект
        self._prj_res_ctrl=ic_user.getKernel().getProjectResController()
        self._prj_res_ctrl.openPrj()
        
        return self._prj_res_ctrl.isRes(TableResName_,'tab')

    def createTableResource(self):
        """
        Построить ресурсное описание по этому компоненту.
        """
        if not self._isTableRes():
            tab_res=self._createTabSpc()
            
            children_fld=self._getChildrenFields()
            for child_fld in children_fld:
                fld_spc=self._createFieldSpc(child_fld)
                tab_res['child'].append(fld_spc)
            self._saveTabRes(tab_res)
            
    def _saveTabRes(self,TabRes_):
        """
        Сохранить ресурс результирующе йтаблицы.
        """
        table_name=TabRes_['name']
        #Сохранить ресурс
        self._prj_res_ctrl.saveRes(table_name,'tab',TabRes_)
        #И сразу удалить за ненадобностью
        self._prj_res_ctrl=None
        
    def _getChildrenFields(self):
        """
        Описание дочерних полей.
        """
        return filter(lambda chld: chld['type']==CONVERTFIELD_TYPE,self.resource['child'])
        
    def _createTabSpc(self,TableName_=None):
        """
        Создать спецификацию результирующей таблицы.
        @param TableName_: Имя результирующей таблицы.
        """
        tab_spc=util.icSpcDefStruct(util.DeepCopy(ic_tab_wrp.ic_class_spc),None)
        #Установить свойства таблицы
        if TableName_ is None:
            TableName_=self.getTableName()
        tab_spc['name']=TableName_
        tab_spc['description']=self.resource['description']
        tab_spc['table']=TableName_.lower()
        tab_spc['source']=self.getDBName()

        return tab_spc

    def _createFieldSpc(self,ConvertFieldSpc_):
        """
        Создать спецификацию поля результирующей таблицы из поля конвертации.
        """
        field_spc=util.icSpcDefStruct(util.DeepCopy(ic_field_wrp.ic_class_spc),None)
        field_spc['name']=ConvertFieldSpc_['name']
        field_spc['description']=ConvertFieldSpc_['description']
        field_spc['field']=ConvertFieldSpc_['field']
        field_spc['type_val']=ConvertFieldSpc_['type_val']
        field_spc['len']=ConvertFieldSpc_['len']
        field_spc['attr']=ConvertFieldSpc_['attr']
        field_spc['default']=ConvertFieldSpc_['default']

        return field_spc
   
    def convert(self):
        """
        Запуск конвертации.
        """
        self.createTableResource()
        
        #Определить базисное поле. 
        #Поле относительно которого будет производится итерация записей.
        basis_field=self.getFirstField()
        if basis_field:
            #Определить драйвер
            driver=basis_field.initDriver()
            #print '<<<!>>>',driver
            fields=self.getFields()
            #Проинициализирогвать все драйвера в полях
            for field in fields:
                field.initDriver()
            
            #self._tab=ic_sqlobjtab.icSQLObjTabClass(self.getTableName())
            self._tab=icsqlalchemy.icSQLAlchemyTabClass(self.getTableName())
            if self.getAutoClear():
                self._tab.clear()
                
            #Перебор по записям
            driver.First()
            print('START!',driver.IsEnd())
            while not driver.IsEnd():
                print('.', end=' ')
                #Перебор по полям и формирование результирующей записи
                rec={}
                for field in fields:
                    value=field.getValue()
                    field_name=field.getName()
                    #print '<<<!>>>',field_name,value
                    rec[field_name]=value
                #Сохранить сформированную запись в результирующей таблице.
                #print '$$$',rec
                self._tab.add(**rec)
                
                driver.Next()            
            print('OK')

    def getFirstField(self):
        """
        Первое поле.
        """
        return None
        
    def getField(self):
        """
        Список полей.
        """
        return None
        
    def getDriver(self):
        """
        Объект драйвера источника данных.
        """
        return None
        
class icConvertFieldPrototype:
    """
    Класс поля конвертера данных в табличное представление.
    """
    def __init__(self,ParentConvertQuery_,component_spc=None):
        """
        Конструктор.
        """
        self.resource=component_spc
        
        self._convert_query=ParentConvertQuery_

        #Драйвер источника данных
        self._driver=None
        #self.initDriver()
        #print 'ZZZ',self.getName(),self._driver,self._convert_query.getDriver()
        
    def getName(self):
        """
        Имя объекта.
        """
        return self.resource['name']
        
    def getDriverName(self):
        """
        Имя драйвера источника данных.
        """
        return self.resource['driver']
        
    def getDriver(self):
        """
        Объект драйвера источника данных.
        """
        return None
        
    def initDriver(self):
        """
        Инициализация объекта драйвера источника данных.
        """
        self._driver=self.getDriver()
        if self._driver is None:
            self._driver=self._convert_query.getDriver()
        return self._driver

    def getSrcName(self):
        """
        Имя поля в источнике.
        """
        return self.resource['src_name']
        
    def getDefault(self):
        """
        Значение поля по умолчанию.
        """
        return self.resource['default']
        
    def getGetValueFunc(self):
        """
        Функцмя получения значения.
        """
        return self.resource['getvalue']
        
    def getValue(self):
        """
        Текущее значение.
        """
        if self._driver:
            src_name=self.getSrcName()
            getvalue=self.getGetValueFunc()
            if getvalue:
                #Выполнение функции получения данных
                evs=util.InitEvalSpace({'self':self,'driver':self._driver,'src_name':src_name})
                return util.ic_eval(getvalue,evalSpace=evs)[1]
            elif src_name:
                return self._driver.getDataByName(src_name)
            else:
                return self.getDefault()
        return None
        
