'''
데이터를 여러 시트로 분해 후 한 개의 pdf 파일로 변환
'''

import win32com.client
import os, glob
from PyPDF2 import PdfFileMerger, PdfFileReader


def convert_excel_to_pdf():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True

    excel_file = '1,xlsx'
    xlsx_path = os.path.join(os.path.abspath(''), excel_file)

    wb = excel.Workbooks.Open(xlsx_path)
    ws_print = wb.Worksheets('print')
    data_list = wb.Worksheets('data').UsedRange()
    for index, i in enumerate(data_list):
        ws_print.Range('b3').value = data_list[index][0] #첫 열을 시트 이름으로 변경
        if not os.path.exists(os.path.abspath('pdf')): #하위 pdf폴더 존재여부 확인 후 생성
            os.mkdir(os.path.abspath('pdf'))

        filename = data_list[index][0] #각 시트 pdf 파일로 변환
        wb.Activesheet.ExportasFixedFormat(0, os.path.join(os.path.abspath('pdf'),f'{filename}'))

    wb.Close(SaveChanges=False) # 저장안함 SaveChanges = True or False
    excel.Quit()

def pdf_merge(): #모든 pdf 파일 병합

    pdf_files = glob.glob(os.path.abspath('pdf')+'\\*.pdf')

    merger = PdfFileMerger()
    for i in pdf_files:
        merger.append(PdfFileReader(open(i, 'rb')))

    merger.write(os.path.join(os.path.abspath(''),'merge.pdf'))

if __name__ == "__main__":
    convert_excel_to_pdf()
    pdf_merge()

