import win32com.client
import os,glob,re, itertools
from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader

class excel_crawlling:
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.excel.Visible = True
        self.sht = self.excel.activesheet

    def usedrange_col(self, col: int):
        list = self.sht.UsedRange()
        return [x[col] for x in list]
        
    def lastcell(self):
        last_col=self.sht.UsedRange.SpecialCells(11).Column
        last_row=self.sht.UsedRange.SpecialCells(11).Row
        last_col_label = chr(int(last_col-1) + 65)
    
        return last_row,last_col 

    def loadcell(self, x, y):
        value = self.sht.Cells(x, y)
        return value

    def savecell(self, x, y, data):
        self.sht.Cells(x, y).value = data

##filter 함수
class Excel_Filter:
    """print = print Sheet number > 1 \n
    db = db Sheet number >1
    """
    def __init__(self,print:int, db:int) -> None:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        self.sht_print = excel.sheets(print)
        self.sht_db = excel.sheets(db)
        
    def get_keyword(self, range:str)->list: 
        #sht_db_get = sht_db.Range("a1").CurrentRegion
        keyword = self.sht_print.Range(range).Value[0]
        keyword= [x for x in keyword if x is not None]
        return keyword

    def get_db(self,range:str="a1")-> tuple:
        sht_db_get = self.sht_db.Range(range).CurrentRegion.Value
        return sht_db_get
  
    def filter_list(self, keyword:str, db_list:list)->list:
        keyword = re.compile(r'.{0,100}'+keyword+r'.{0,100}')
        result_list= [] 
        result_text=''
        for rows in db_list:
            for item in rows:
                result_text += str(item)
            if keyword.findall(result_text):
                result_list.append(rows)
            result_text=''
        return result_list

    def print_result(self, result_list:list,currentregion:str="a1")->None:
        old_result = self.sht_print.Range(currentregion).CurrentRegion
        old_result.Clear()
        col_regexp=r'[a-zA-z]+'
        row_regexp=r'\d+'
        printcol = int(ord(re.findall(col_regexp,currentregion)[0])-ord('a')+1)
        printrow = int(re.findall(row_regexp,currentregion)[0])
        self.sht_print.Range(self.sht_print.Cells(printrow,printcol),
         self.sht_print.Cells(len(result_list)+printrow-1,
         len(result_list[0])+printcol-1)).value = result_list

#행단위 pdf 파일 변환
class Excel_to_Pdf:
    def __init__(self) -> None:
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.excel.Visible = True # 진행과정 보기
    def loadfile(self, file:str)->None:
        xlsx_path = os.path.join(os.path.abspath(''),file)
        self.wb  = self.excel.Workbooks.Open(xlsx_path)
    def loadsheet(self, sheet:str)->None:
        self.ws = self.wb.Worksheets(sheet)
    def copydata(self):
        for i in self.ws.UsedRange():
            new_sht = self.wb.Worksheets.Add()
            new_sht.name = i[0] #1열 데이터 시트 이름으로 변경
            new_sht.Range('a1:f1').value = i #행 데이터 복사
    def PdfSave(self):
        for i in self.ws.UsedRange():
            ws = self.wb.Worksheets(i[0])
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
            self.wb.Activesheet.ExportasFixedFormat(0, os.path.join(os.path.abspath('pdf'),f'{filename}'))
        self.wb.Close(SaveChanges=False) # 저장안함 SaveChanges = True or False
        self.excel.Quit()

#명세서 pdf 변환
class Excel_to_OneCell_Pdf:
    def __init__(self) -> None:
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.excel.Visible = True

    def loadfile(self, file)->None:
        xlsx_path = os.path.join(os.path.abspath(''), file)
        self.wb = self.excel.Workbooks.Open(xlsx_path)

    def pdfsave(self, print_sheet:str='print', data_sheet:str='data')->None:
        ws_print = self.wb.Worksheets(print_sheet)
        data_list = self.wb.Worksheets(data_sheet).UsedRange()
        for index, i in enumerate(data_list):
            ws_print.Range('b3').value = data_list[index][0] #첫 열을 시트 이름으로 변경
            if not os.path.exists(os.path.abspath('pdf')): #하위 pdf폴더 존재여부 확인 후 생성
                os.mkdir(os.path.abspath('pdf'))

            filename = data_list[index][0] #각 시트 pdf 파일로 변환
            self.wb.Activesheet.ExportasFixedFormat(0, os.path.join(os.path.abspath('pdf'),f'{filename}'))

        self.wb.Close(SaveChanges=False) # 저장안함 SaveChanges = True or False
        self.excel.Quit()

    def PdfMerge(self,outputfile:str='merge.pdf')->None:
        pdf_files = glob.glob(os.path.abspath('pdf')+'\\*.pdf') #pdf 폴더 pdf파일 리스트 저장
        merger = PdfFileMerger()
        for i in pdf_files:
            merger.append(PdfFileReader(open(i, 'rb')))
        merger.write(os.path.join(os.path.abspath(''),outputfile))

class Excel_Folder_File_List:
    def __init__(self) -> None:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        self.sht = excel.activesheet

    def filelist(self, path:str)->list:
        path = Path(path)
        filelist= os.listdir(path)
        list_data= []
        for i in filelist:
            list_data.append([i])
        return list_data

    def writedata(self, data:list,row:int=1, col:int=1):
        self.sht.Range(self.sht.Cells(row,col),self.sht.Cells(len(data)+row-1,col)).value=data

##데이터 중복 제거
class Excel_DedupLication:
    def __init__(self) -> None:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        self.sht = excel.activesheet
        

    def position(self, old:str='a1', new:str='a1', search_col:str='a'):
        self.new = new
        curnt_db = self.sht.Range(old).currentregion.value
        self.curnt_db = list(itertools.chain(*curnt_db))
        self.new_db = self.sht.Range(new).currentregion.value

        col_regexp=r'[a-zA-z]+'
        row_regexp=r'\d+'
        self.col = int(ord(re.findall(col_regexp,new)[0])-ord('a')+1)
        self.row = int(re.findall(row_regexp,new)[0])
        self.search_col_num = int(ord(re.findall(col_regexp,search_col)[0])-ord('a'))

    def Deduplication(self):
        new_list = []
        for i in self.new_db:
            if not i[self.search_col_num] in self.curnt_db: #중복 기준 열 i[]
                new_list.append(i)

        self.sht.Range(self.new).currentregion.Clear()
        self.sht.Range(self.new, self.sht.Cells(len(new_list)+self.row-1, len(new_list[0]))).value = new_list
