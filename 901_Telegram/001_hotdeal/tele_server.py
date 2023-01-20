from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
import command_menu
from datetime import datetime
from info import token #텔레그램 봇 token 값 호출 변겯 요망

token = token()


updater = Updater(token, use_context=True)

def add_handler(cmd, func):
    updater.dispatcher.add_handler(CommandHandler(cmd, func))
    
def message_handler(func):
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), func))\

def add_button_handdler(func):
    updater.dispatcher.add_handler(CallbackQueryHandler(func))
    
def add_handler_list():
    list = {
        'id' : command_menu.user_id,
        'add' : command_menu.create_user,
        'site_list' : command_menu.site_list,
        'site_add' : command_menu.site_add,
        'site_del' : command_menu.site_del,
        'site_clean' : command_menu.site_clean,
        'alert' : command_menu.force_alert,
        'db_update' : command_menu.db_update,
        'command_list' : command_menu.command_list,
    }
    return list

def start_bot():
    print(f'start_bot_main [{datetime.now()}]')
    
    for key, value in add_handler_list().items():
        add_handler(key, value)
    
    add_button_handdler(command_menu.callback)
    #message_handler(command_menu.get_message)
       
    updater.start_polling(timeout=5, clean=True)
    updater.idle()
    
    
if __name__ == '__main__':
    start_bot()
