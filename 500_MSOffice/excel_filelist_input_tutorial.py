from lib.excel import Excel_Folder_File_List as ex

PATH='C:\\Users\\ardi\\Downloads'
excel =ex()
data = excel.filelist(PATH)
excel.writedata(data,3,1)
