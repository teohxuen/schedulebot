from scheduler import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def botinit(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi I'm a bot that help to generate schedules to help you visualise better. Call '/help' for instructions!")

def bothelp(update, context):
    message = 'Please enter your message as shown:\n' +\
            '/make\n'+\
            '<calendar start><calendar end>\n'+\
            '<vehicles>\n'+\
            '<event start>,<veh used>:<event name>,<event end>\n'+\
            'Additionally, you can omit the event end date if the event is a 1 day event.'
    example = '/make\n'+\
            '10 Aug 20 24 Aug 20\n'+\
            'Car 1, Car 2, Car 3, Car 4\n'+\
            '11 Aug, Car 1: Quarterly Checks, 13 Aug\n'+\
            '17 Aug, Car 2: Annual Checks\n'+\
            '18 Aug, Car 3: Quarterly Checks, 19 Aug\n'+\
            '20 Aug, Car 4: Annual Checks\n'+\
            '24 Aug, Holiday!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Here's an example: ")
    context.bot.send_message(chat_id=update.effective_chat.id, text=example)

def botschedule(update,context):
    filepath = scheduler(update.message.text, update.effective_chat.id, context)
    if filepath:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here's your picture!")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'{filepath}/out{update.effective_chat.id}.jpg', 'rb'))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unfortunately we are unable to generate the schedule, check out /help for assistance")

def main():

    updater = Updater(token='YOUR TOKEN HERE', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', botinit)
    dispatcher.add_handler(start_handler) 

    help_handler = CommandHandler('help', bothelp)
    dispatcher.add_handler(help_handler) 

    scheduler_handler = CommandHandler('make', botschedule)
    dispatcher.add_handler(scheduler_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

    print("Bot is running! BEEP BOOP!")  


main()
