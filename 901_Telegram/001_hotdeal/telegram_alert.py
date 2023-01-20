from datetime import datetime
import telegram
import sql
from code_dict import site_code
from info import token  # token값 호출 변경 요망

token = token()

bot = telegram.Bot(token=token)


def telegram_send():
    user_info = sql.all_user_info()
    id = user_info[1]
    load_site = user_info[2].split(',')
    index = user_info[3]

    db = sql.select_alert_site(index)
    max_index = []

    for j in db:
        if j[1] in load_site:
            title = site_code(j[1], 'site_name')[2]
            text = f'제목({title}) : {j[2]}  \n {j[4]}{j[3]}'
            bot.send_message(chat_id=id, text=text)
            max_index.append(j[0])
        try:
            sql.update_user_info_site_index(id, max(max_index))
        except ValueError:
            pass


def alert_bot():
    print(f'start_alert_bot [{datetime.now()}]')
    telegram_send()
