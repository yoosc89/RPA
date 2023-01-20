from lib.excel import Excel_Filter

def main():
    excel_filter=Excel_Filter(1,2)
    keyword = excel_filter.get_keyword("b1:d1")
    get_db = excel_filter.get_db("a1")
    
    if len(keyword)==1:
        get_db = excel_filter.filter_list(keyword[0], get_db)
   
    else:
        for i in keyword:
            get_db = excel_filter.filter_list(i, get_db)
        

    return excel_filter.print_result(result_list=get_db,
        currentregion="a3")

if __name__ == '__main__':
    main()

