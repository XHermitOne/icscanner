#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции манипулирования PDF файлами.

Функции основаны на библиотеке PyPDF2
Установка:
****************************************************
sudo apt-get install python-pypdf2
****************************************************

Краткая документация
(оригинал https://reachtim.com/articles/PDF-Manipulation.html#manipulating-pypdf2):

Manipulating: PyPDF2
---------------------

You can manipulate PDF files in a variety of ways using the
pure-Python PyPDF2 toolkit. The original pyPDF library is
officially no longer being developed but the pyPDF2 library
has taken up the project under the new name and continues
to develop and enhance the library. The development team is
dedicated to keeping the project backward compatible. Install with pip.

Want to merge two PDFs?
Merge can mean a couple of things—you can merge,
in the sense of inserting the contents of one PDF after
the content of another, or you can merge by applying one
PDF page on top of another.

Merge (layer)
--------------

For an example of the latter case, if you have a one-page PDF containing
a watermark, you can layer it onto each page of another PDF.
Say you’ve created a PDF with transparent watermark text
(using Photoshop, Gimp, or LaTeX). If this PDF is named wmark.pdf,
the following python code will stamp each page of the target PDF with the watermark.

**************************************************************************
from PyPDF2 import PdfFileWriter, PdfFileReader
output = PdfFileWriter()

ipdf = PdfFileReader(open('sample2e.pdf', 'rb'))
wpdf = PdfFileReader(open('wmark.pdf', 'rb'))
watermark = wpdf.getPage(0)

for i in xrange(ipdf.getNumPages()):
    page = ipdf.getPage(i)
    page.mergePage(watermark)
    output.addPage(page)

with open('newfile.pdf', 'wb') as f:
   output.write(f)
**************************************************************************

If your watermark PDF is not transparent it will hide the underlying text.
In that case, make sure the content of the watermark displays on the header
or margin so that when it is merged, no text is masked.
For example, you can use this technique to stamp a logo or letterhead on
each page of the target PDF.

Merge (append)
---------------

This snippet takes all the PDFs in a subdirectory named mypdfs and
puts them in name-sorted order into a new PDF called output.pdf

**************************************************************************
from PyPDF2 import PdfFileMerger, PdfFileReader
import os

merger = PdfFileMerger()
files = [x for x in os.listdir('mypdfs') if x.endswith('.pdf')]
for fname in sorted(files):
    merger.append(PdfFileReader(open(os.path.join('mypdfs', fname), 'rb')))

merger.write("output.pdf")
**************************************************************************

Delete
-------

If you want to delete pages, iterate over the pages in your source
PDF and skip over the pages to be deleted as you write your new PDF.
For example, if you want to get rid of blank pages in source.pdf:

**************************************************************************
from PyPDF2 import PdfFileWriter, PdfFileReader
infile = PdfFileReader('source.pdf', 'rb')
output = PdfFileWriter()

for i in xrange(infile.getNumPages()):
    p = infile.getPage(i)
    if p.getContents(): # getContents is None if  page is blank
        output.addPage(p)

with open('newfile.pdf', 'wb') as f:
   output.write(f)
**************************************************************************

Since blank pages are not added to the output file, the result is that
the new output file is a copy of the source but with no blank pages.

Split
------

You want to split one PDF into separate one-page PDFs.
Create a new file for each page and write it to disk as you
iterate through the source PDF.

**************************************************************************
from PyPDF2 import PdfFileWriter, PdfFileReader
infile = PdfFileReader(open('source.pdf', 'rb'))

for i in xrange(infile.getNumPages()):
    p = infile.getPage(i)
    outfile = PdfFileWriter()
    outfile.addPage(p)
    with open('page-%02d.pdf' % i, 'wb') as f:
        outfile.write(f)
**************************************************************************

Slices
-------

You can even operate on slices of a source PDF, where each
item in the slice is a page.

Say you have two PDFs resulting from scanning odd and even pages
of a source document. You can merge them together, interleaving the pages as follows:

**************************************************************************
from PyPDF2 import PdfFileWriter, PdfFileReader
even = PdfFileReader(open('even.pdf', 'rb'))
odd = PdfFileReader(open('odd.pdf', 'rb'))
all = PdfFileWriter()
all.addBlankPage(612, 792)

for x,y in zip(odd.pages, even.pages):
    all.addPage(x)
    all.addPage(y)

while all.getNumPages() % 2:
    all.addBlankPage()

with open('all.pdf', 'wb') as f:
    all.write(f)
**************************************************************************

The first addBlankPage (line 5) insures that the output PDF begins
with a blank page so that the first content page is on the right-hand side.
Note that, when you add a blank page, the default page dimensions are
set to the previous page. In this case, because there is no previous page,
you must set the dimensions explicitly; 8.5 inches is 612 points, 11 inches is 792 points).
Alternatively, you might add a title page as the first page.
In any case, putting the first content page on the right-hand side
(odd numbered) is useful when your PDFs are laid out for a two-page (book-like) spread.

The last addBlankPage sequence (lines 11-12) insures there is an even
number of pages in the final PDF. Like the first addBlankPage,
this is an optional step, but could be important depending on how the
final PDF will be used (for example, a print shop will appreciate that your
PDFs do not end on an odd page).
"""

import os
import os.path
import PyPDF2

from ic.std.log import log

__version__ = (0, 0, 1, 2)


def glue_pdf_files(out_pdf_filename, *pdf_filenames):
    """
    Процедура склеивания/объединения PDf файлов в один.
    @param out_pdf_filename: Полное наименование результирующего PDF файла.
    @param pdf_filenames: Список имен файлов-источников.
        Объединение происходит в порядке указанном списком pdf_filenames.
        Если какой либо файл отсутствует, то объединение происходит без него.
    @return: True - объединение прошло успешно / False - ошибка по какой-либо причине.
    """
    try:
        merger = PyPDF2.PdfFileMerger()
        filenames = [filename for filename in pdf_filenames
                     if filename.lower().endswith('.pdf') and os.path.exists(filename)]
        for filename in filenames:
            pdf_file = open(filename, 'rb')
            log.debug(u'Объединение PDF файла <%s> => <%s>' % (out_pdf_filename, filename))
            reader = PyPDF2.PdfFileReader(pdf_file)
            merger.append(reader)

        merger.write(out_pdf_filename)
        return True
    except:
        log.fatal(u'Ошибка склеивания/объединения PDF файлов')
    return False
