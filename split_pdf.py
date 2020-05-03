import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import easygui


def main():
    pdffile = easygui.fileopenbox(title="PDF Splitter",
                                  msg="Select file to split",
                                  filetypes="*.pdf",
                                  multiple=False)
    if not pdffile or not pdffile.endswith(".pdf"):
        exit(-1)
    pages_str = easygui.enterbox(title="PDF Splitter",
                                 msg="Select pages to split (e.g. 10-15,157-158)")
    if not pages_str or '-' not in pages_str:
        exit(-1)
    assert pages_str.count('-') - pages_str.count(',') == 1, "Use ',' for multiple splits"
    pages = pages_str.split(',')

    pdf = PdfFileReader(pdffile)

    for p in pages:
        p_start = int(p.split('-')[0]) if p.split('-')[0] else 1
        p_end = int(p.split('-')[1]) if p.split('-')[1] else None
        assert p_start < pdf.getNumPages(), "Starting page greater than total number of pages"
        if p_end > pdf.getNumPages() or not p_end:
            print "Ending page greater than total number of pages. Selecting the last page instead."
            p_end = pdf.getNumPages()

        file_out = os.path.splitext(pdffile)[0] + "_pages{}-{}.pdf".format(p_start, p_end)
        pdf_writer = PdfFileWriter()

        for pp in range(p_start, p_end + 1, 1):
            pdf_writer.addPage(pdf.getPage(pp - 1))

        with open(file_out, 'wb') as fout:
            pdf_writer.write(fout)
        print "Created: {}".format(os.path.basename(file_out))

    more = raw_input("Finished! Do you want to split more? (y/n):\n")
    return more == 'y'


if __name__ == '__main__':
    print "Staring PDF Splitter"
    split_more = True
    while split_more:
        split_more = main()
