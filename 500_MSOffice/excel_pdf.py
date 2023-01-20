##엑셀 행단위 pdf 파일 변환

import win32com.client
import os


excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True # 진행과정 보기

xlsx_path = os.path.join(os.path.abspath(''),'1.xlsx')
wb  = excel.Workbooks.Open(xlsx_path)


ws1 = wb.Worksheets("Sheet1")

for i in ws1.UsedRange():
    new_sht = wb.Worksheets.Add()
    new_sht.name = i[0] #1열 데이터 시트 이름으로 변경
    new_sht.Range('a1:f1').value = i #행 데이터 복사

for i in ws1.UsedRange():
    ws = wb.Worksheets(i[0])
    ws.Select()
    ws.PageSetup.Orientation = 2 #인쇄 방향
    wb_temp = ws.Range('a1:f1')
    wb_temp.Columns.Autofit # 열 글자 셀크기 자동맞춤
    wb_temp.Borders.Linestyle= 1 #선스타일
    wb_temp.Borders.ColorIndex = 1 #색상
    wb_temp.Borders.Weight = 1 #선 굵기

    if not os.path.exists(os.path.abspath('pdf')):
        os.mkdir(os.path.abspath('pdf'))

    filename = i[0]
    wb.Activesheet.ExportasFixedFormat(0, os.path.join(os.path.abspath('pdf'),f'{filename}'))

wb.Close(SaveChanges=False) # 저장안함 SaveChanges = True or False

excel.Quit()