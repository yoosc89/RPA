import os
import platform
from lib.google_sheet import google_sheet

def input_info():
    info = input('입력 하세요~ : ')
    url =['https://docs.google.com/spreadsheets/d/1OEOZeNlVwjAqqf-LQVVKeRLvEapatdQy7LVIcaRJQKc/edit#gid=0','https://docs.google.com/spreadsheets/d/1OpdG001cYyEVcmScDf3U-R8W9IuaDWacAVYZnABaQR4/edit#gid=0']
    nextbool='a'
    terminal_clear()
    for url in url:
        if nextbool == 'a' or nextbool == 'ㅁ'  :
            result = google_sheet().worksheet_loads(url)
            google_sheet().sheets_result_pandas(result,info)
            nextbool = input('next : a, end : enter ')
        else:
            break

def terminal_clear():
    os_name = platform.system()
    if os_name == 'Darwin':
        os.system('clear')
    else:
        os.system('cls')

if __name__ == '__main__':
    while True:
       input_info()
       
 