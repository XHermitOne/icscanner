#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль конвертора файлов Excel в xml формате в словарь.
"""

# Подключение библиотек
import sys

from xml.sax import xmlreader
import xml.sax.handler

from ic.std.log import log

__version__ = (0, 0, 1, 2)


def XmlFile2Dict(XMLFileName_):
    """
    Функция конвертации файлов Excel в xml формате в словарь Python.
    @param XMLFileName_: Имя xml файла. 
    @return: Функция возвращает заполненный словарь, 
        или None в случае ошибки.
    """
    xml_file = None
    try:
        xml_file = open(XMLFileName_, 'r')

        input_source = xmlreader.InputSource()
        input_source.setByteStream(xml_file)
        xml_reader = xml.sax.make_parser()
        xml_parser = icXML2DICTReader()
        xml_reader.setContentHandler(xml_parser)
        # включаем опцию namespaces
        xml_reader.setFeature(xml.sax.handler.feature_namespaces, 1)
        xml_reader.parse(input_source)
        xml_file.close()

        return xml_parser.getData()
    except:
        if xml_file:
            xml_file.close()
        info = sys.exc_info()[1]
        log.fatal(u'Ошибка чтения файла <%s> : <%s>.' % (XMLFileName_, info))
        return None


class icXML2DICTReader(xml.sax.handler.ContentHandler):
    """
    Класс анализатора файлов Excel-xml формата.
    """
    def __init__(self, *args, **kws):
        """
        Конструктор.
        """
        xml.sax.handler.ContentHandler.__init__(self, *args, **kws)

        # Выходной словарь
        self._data = {'name': 'Excel', 'children': []}
        # Текущий заполняемый узел
        self._cur_path = [self._data]

        # Текущее анализируемое значение
        self._cur_value = None

    def getData(self):
        """
        Выходной словарь.
        """       
        return self._data

    def _eval_value(self, value):
        """
        Попытка приведения типов данных.
        """
        if isinstance(value, unicode):
            value = value.encode('CP1251')
        try:
            # Попытка приведения типа
            return eval(value)
        except:
            # Скорее всего строка
            return value
        
    def characters(self, content):
        """
        Данные.
        """
        if content.strip():
            if self._cur_value is None:
                self._cur_value = ''
            self._cur_value += content.encode('CP1251')

    def startElementNS(self, name, qname, attrs):
        """
        Разбор начала тега.
        """
        # Имя элемента задается кортежем
        if isinstance(name, tuple):
            # Имя элемента
            element_name = name[1].encode('CP1251')
            # Создать структуру,  соответствующую элементу
            self._cur_path[-1]['children'].append({'name': element_name, 'children': []})
            self._cur_path.append(self._cur_path[-1]['children'][-1])
            cur_node = self._cur_path[-1]
            # Имена параметров
            element_qnames = attrs.getQNames()
            if element_qnames:
                # Разбор параметров элемента
                for cur_qname in element_qnames:
                    # Имя параметра
                    element_qname = attrs.getNameByQName(cur_qname)[1].encode('CP1251')
                    # Значение параметра
                    element_value = attrs.getValueByQName(cur_qname).encode('CP1251')
                    cur_node[element_qname] = element_value

    def endElementNS(self, name, qname): 
        """
        Разбор закрывающего тега.
        """
        # Сохранить проанализированное значение
        if self._cur_value is not None:
            self._cur_path[-1]['value'] = self._cur_value
            self._cur_value = None
            
        del self._cur_path[-1]

if __name__ == '__main__':
    rep_file = None
    xml_file = None
    xml_file = open(sys.argv[1], 'r')

    input_source = xmlreader.InputSource()
    input_source.setByteStream(xml_file)
    xml_reader = xml.sax.make_parser()
    xml_parser = icXML2DICTReader()
    xml_reader.setContentHandler(xml_parser)
    # включаем опцию namespaces
    xml_reader.setFeature(xml.sax.handler.feature_namespaces, 1)
    xml_reader.parse(input_source)
    print((xml_parser.getData()))
    xml_file.close()
