import telebot
import os
import subprocess
from time import sleep
from gpiozero import CPUTemperature
import gpiozero
from gpiozero.pins.mock import MockFactory

gpiozero.Device.pin_factory = MockFactory()
bot_key = os.environ.get('BOT_HTTPS_KEY')
bot = telebot.TeleBot(bot_key)
flag = 1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    welcome = '''
Send /help to get list of commands'''
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    bot.reply_to(message, "Hello, " + name + "." + welcome)


@bot.message_handler(commands=['help'])
def send_help(message):
    helper = '''Send /temp to get temperature
Send /shutdown to shutdown
Send /reboot to reboot
Send /mem to get Memory
Send /loop to get Cpu temp alerts
Send /stop to stop cpu temp alerts     
    '''
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    bot.reply_to(message, helper)


@bot.message_handler(commands=['temp'])
def send_temp(message):
    cpu = CPUTemperature()
    temp = cpu.temperature
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    bot.reply_to(message, str(temp))


@bot.message_handler(commands=['shutdown'])
def send_shutdown(message):
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    bot.reply_to(message, "Shutting Down")
    subprocess.call('sudo shutdown -h now', shell=True)


@bot.message_handler(commands=['reboot'])
def send_reboot(message):
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    bot.reply_to(message, "Rebooting")
    subprocess.call('sudo reboot', shell=True)


@bot.message_handler(commands=['mem'])
def send_memory(message):
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    memory = subprocess.Popen("free -h", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    bot.reply_to(message, str(memory))


@bot.message_handler(commands=['loop'])
def loop(message):
    while flag:
        cpu = CPUTemperature()
        temp = cpu.temperature
        if temp > 60.0:
            bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
            bot.reply_to(message, "ALERT : CPU Temp is high " + str(temp))
        sleep(3000)


@bot.message_handler(commands=['stop'])
def stop(message):
    global flag
    flag = 0
    bot.get_chat_member(chat_id=1283200303, user_id=message.from_user.id)
    bot.reply_to(message, "stopped")


def call_bot():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    call_bot()
