from pymysql import IntegrityError
import pymysql
import itertools
from info import mysql_account as account  # mysql 계정 정보 호출

host = account()['host']
user = account()['user']
password = account()['password']
db = account()['db']

conn = pymysql.connect(host=host, user=user,
                       password=password, db=db, charset='utf8')
cursor = conn.cursor()


def all_user_info():
    cursor.execute("SELECT * from user_info;")
    return [x for j in cursor.fetchall() for x in j]  # return type list


def select_user_info(telegram_id):
    cursor.execute(
        "select * from user_info where telegram_id = %s;", telegram_id)
    user_info = cursor.fetchall()

    if user_info != ():
        return user_info[0]  # return type tuple
    else:
        return None


def create_user(user_data):
    cursor.execute(
        'insert into user_info(telegram_id, site_list, alert_site_index) values(%s, %s, %s, %s);', user_data)


def insert_user_info(telegram_id, user_site):
    cursor.execute("insert into telegram_bot.user_info (telegram_id, site_list) values (%s,%s);", [
                   telegram_id, [user_site]])
    conn.commit()


def update_user_info_site_index(telegram_id, index):
    cursor.execute("update user_info set alert_site_index = %s where telegram_id = %s;", [
                   index, telegram_id])
    conn.commit()


def update_user_info_site_list(telegram_id, site_list):
    cursor.execute("update user_info set site_list = %s where telegram_id = %s;", [
                   site_list, telegram_id])
    conn.commit()


def select_alert_site(index):
    cursor.execute("select * from alert_site where id > %s;", index)
    return cursor.fetchall()  # return type tuple


def last_index_alert_site():
    cursor.execute("select id from alert_site ORDER BY id DESC limit 1;")
    return cursor.fetchall()


def max_alert_site():
    cursor.execute("select max(id) from alert_site where id")


def insert_alert_site(data):
    index = [i for i in last_index_alert_site()[0]]
    print(index)
    for i in data:
        try:
            index[0] += 1
            cursor.executemany(
                "insert into telegram_bot.alert_site (id, site_name, site_title, site_url, site_domain) values (%s,%s,%s,%s,%s);", [index+i])
        except IntegrityError:
            index[0] -= 1
            pass
    # cursor.execute("SET @CNT = 0;")
    # cursor.execute("UPDATE alert_site SET alert_site.id = @CNT:=@CNT+1;")
    conn.commit()


def delete_alert_site(*site_name):
    if type(site_name[0]) == list:
        site_name = list(itertools.chain(*site_name))
    else:
        pass

    cursor.executemany("delete from alert_site where site_name=%s;", site_name)
    conn.commit()
