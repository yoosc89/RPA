def site_code(search, search_type):
    
    site_code = [
            ['01001','clien_jirum','클리앙-알뜰구매'],
            ['01002','ppomppu', '뽐뿌게시판'],
            ['01003','jmana', '제이마나'],
            ['01004','quasarzone', '퀘이사존-핫딜'],
            ['01005','ruliweb', '루이웹-핫딜'],
            ['01006','coolenjoy','쿨엔조이-지름,알뜰정보']
        ]

    if search_type == 'code':
        return [x for i in site_code if i[0] == search for x in i]
    elif search_type ==  'site_name':
        return [x for i in site_code if i[1] == search for x in i]
    elif search_type ==  'korea_name':
        return [x for i in site_code if i[2] == search for x in i]
    elif search_type == 'button':
        return  [i for i in site_code if i[0][0:2] == search]
    elif search_type == 'all':
        return site_code
    else:
        return None

def command_text():
    command_text = """
1. /id : 계정 고유 아이디 출력
2. /add : 봇 채널 계정 등록 !!알림 받기 위해서는 필수로 입력!!
3. /site_list : 등록가능한 사이트 목록
3. /site_add : 알림 사이트 등록
4. /site_del : 알림 사이트 등록 제거
5. /site_clean : 알림 사이트 초기화
6. /db_update : 디비 업데이트
7. /alert : 강제 알림
8. /command_list : 명령어 출력
"""
    return command_text