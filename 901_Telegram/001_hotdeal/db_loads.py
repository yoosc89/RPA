import sql
import re
from code_dict import site_code


def type_code(code):
    type_code = {
        '01' : site_add,
        '02' : site_del,
    }
    return type_code[code[0:2]]


def user_db_load(telegram_id):
    user_loads = sql.select_user_info(telegram_id)
    try:
        user_id = user_loads[1]
        site_list = user_loads[2].split(',')
        site_index = user_loads[3]
        return user_id, site_list, site_index
    except TypeError:
        return None, None

    except IndexError:
        return None, None

def site_list(telegram_id):
    site_list = list(sql.select_user_info(telegram_id))[2].split(',')
    m_list = ''
    for index, i in enumerate(site_list, 1):
        m_list +=f'{index}. ' + site_code(i,'site_name')[2] +' \n '

    return m_list #return string

def create_user(telegram_id):
    user = sql.select_user_info(telegram_id)
    if user == None:
        sql.create_user([telegram_id, 0, sql.max_alert_site])
        return 0
    else:
        return 1


def serach_user_info(telegram_id):
    return sql.select_user_info(telegram_id)



def site_add(telegram_id, data):
    sql_list = sql.select_user_info(telegram_id)[2]
    
    if data in sql_list:
        title = site_code(data, 'site_name')[2]
        echo = f'{title}은(는) 이미 등록한 사이트 입니다.'
        return echo
    else:
        sql_list += data+','
        sql.update_user_info_site_list(telegram_id, sql_list)
        title = site_code(data, 'site_name')[2]
        echo = f'{title}을(를) 등록이 완료했습니다.'
        return echo
    
    
def site_del(telegram_id, data):
    sql_list = sql.select_user_info(telegram_id)[2]
    echo = ''
    if data in sql_list:
        sql_list = re.sub(data+',','',sql_list)
        title = site_code(data, 'site_name')[2]
        echo = f'{title}(을)를 삭제하였습니다'
        sql.update_user_info_site_list(telegram_id, sql_list)
    else:
        title = site_code(data, 'site_name')[2]
        echo = f'{title}(은)는 등록되어 있지 않습니다.'
    
    return echo

def site_clean(telegram_id):
    site_lst = ''
    sql.update_user_info_site_list(telegram_id, site_lst)
    return 1