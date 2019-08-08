import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
import selectparser

PageSelect = selectparser.PageSelect

class Pdf():

    def __init__(self, pdfpath):
        reader = PdfFileReader(pdfpath)
        self.pages = [reader.getPage(i) for i in range(reader.getNumPages())]

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.pages[i]
        if not isinstance(i, PageSelect):
            raise TypeError('indices must be int or PdfSelect, not ' + type(i))
        start = i.start
        end = i.end
        rotate = i.rotate
        if end == None:
            end = start
        rv_list = self.pages[start:end+1]
        if i.rotate is not None:
            for p in rv_list:
                p.rotateClockwise(rotate)
        return rv_list

def copy_page(page):
    w = PdfFileWriter()
    w.addPage(page)

def recombine(pdfpaths, selects):
    pdfs = [Pdf(pdfpaths[i.id_]) for i in selects]
    pages = []
    for i, s in enumerate(selects):
        pages.extend(pdfs[i][s])
    w = PdfFileWriter()
    for p in pages:
        w.addPage(p)
    return w

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: ' + sys.argv[0] + ' [input_files] output_file expr')
        sys.exit(-1)
    expr = sys.argv[-1]
    file_list = sys.argv[1:-2]
    output = sys.argv[-2]

    selects = selectparser.get_selects(expr)
    writer = recombine(file_list, selects)
    with open(output, 'wb') as f:
        writer.write(f)
