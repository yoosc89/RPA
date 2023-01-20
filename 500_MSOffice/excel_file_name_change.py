import os
import shutil
from lib.excel import excel_crawlling

DIR = 'C:\\Users\\ardi\\Desktop\\projec\\site_parser'
ec = excel_crawlling()

name_list = ec.usedrange_col(1)
file_name = '_name.text'

for index, i in enumerate(name_list, 1):
    old_file = os.path.join(DIR, i+file_name)
    new_file = os.path.join(DIR, str(index)+i+file_name)
    shutil.move(old_file, new_file)
    ec.savecell(index, 1, index)
