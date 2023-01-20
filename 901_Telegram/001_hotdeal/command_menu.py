import telegram_alert
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import db_loads
from parser_list import parser_db2
from code_dict import site_code, command_text


def command_list(update, context):
    update.message.reply_text(command_text())


def get_message(update, context):
    update.message.reply_text("text")
    update.message.reply_text(update.message.chat.id)
    print(update.message)


def create_user(update, context):
    user = db_loads.create_user(update.message.chat.id)
    if user == 1:
        update.message.reply_text("이미 계정이 등록되어 있습니다")
    elif user == 0:
        update.message.reply_text("계정이 등록되었습니다")
    else:
        update.message.reply_text(f"알 수 없는 오류가 발생했습니다 : ")


def db_update(update, context):
    parser_db2()
    update.message.reply_text("db 업데이트 완료 되었습니다.")


def site_list(update, context):
    list_message = 'Index | Site_Name | Commnad\n'

    for index, i in enumerate(site_code('', 'all'), 1):

        list_message += f'{index} | {i[2]} | {i[1]}\n'

    update.message.reply_text(f'등록 가능한 사이트 목록 : \n{list_message}')


def user_id(update, context):
    info = list(db_loads.serach_user_info(update.message.chat.id))
    print(info)
    Message = f'USER ID : {info[1]}\nSITE_LIST : {info[2]}\nINDEX NUMBER : {info[3]}'
    update.message.reply_text(Message)


def force_alert(update, context):
    telegram_alert.telegram_send()
    update.message.reply_text('전송 완료 했습니다.')


def site_del(update, context):
    type_code = '02'
    currunt_Slist = list(db_loads.serach_user_info(
        update.message.chat.id))[2].split(',')
    temp_list = []
    buttons = []

    for i in currunt_Slist:
        site_list = site_code(i, 'site_name')
        if site_list != []:
            temp_list.append(site_code(i, 'site_name'))
    buttons = []
    for i in temp_list:
        buttons.append([InlineKeyboardButton(
            i[2], callback_data=type_code+i[0])])

    reply_markup = InlineKeyboardMarkup(buttons)
    if buttons != []:
        context.bot.send_message(
            update.message.chat.id, '삭제할 사이트를 선택하세요', reply_markup=reply_markup)
    else:
        update.message.reply_text('등록된 사이트가 없습니다.')


def site_clean(update, context):
    re = db_loads.site_clean(update.message.chat.id)
    if re == 1:
        update.message.reply_text(f'등록한 사이트 값을 초기화 했습니다')
    else:
        update.message.reply_text(f'알수 없는 오류가 발생했습니다.')


def site_add(update, context):
    type_code = '01'
    site_list = site_code('01', 'button')

    buttons = []
    for i in site_list:
        buttons.append([InlineKeyboardButton(
            i[2], callback_data=type_code+i[0])])

    reply_markup = InlineKeyboardMarkup(buttons)

    context.bot.send_message(update.message.chat.id,
                             '등록할 사이트를 선택하세요', reply_markup=reply_markup)


def callback(update, context):
    callback_code = update.callback_query.data
    site_name = site_code(callback_code[2:], 'code')[1]
    click = db_loads.type_code(callback_code)(
        update.effective_user.id, site_name)
    context.bot.send_message(update.effective_user.id, click)
