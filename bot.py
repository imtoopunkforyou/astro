import telebot
from telebot import types
from conf import TOKEN
import os, shutil
from datetime import datetime, timedelta
from saves_controller import clear_foulder
from os import listdir
from os.path import isfile, join


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def help(message):
    bot.send_message(message.chat.id, 'Привет! Вижу, ты готов начать предновогоднее путшествие в Astroneer'
                     '\nНапиши мне /help')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Список доступных команд:\n'
                     '/start - приветствие\n'
                     '/help - справка \n'
                     '/last - получить последний сейв \n'
                     '/how - что нужно сделать, чтобы поставить себе сейв \n'
                     'Если ты закончил играть у тебя есть сейв - пришли мне файл')

@bot.message_handler(commands=['how'])
def help(message):
    bot.send_message(message.chat.id, '1. Скачай последнее сохранение через команду /last\n'
                     '2. Открой проводник в винде\n' + 
                     '3. Вбей путь %LOCALAPPDATA%\Astro\Saved\SaveGames\n'
                     '4. Удали из этой папки все файлы\n'
                     '5. Положи скаченный файл в эту папку\n'
                     '6. Запусти игру и напиши ребятам, чтобы присоеденились :)')
    
@bot.message_handler(content_types=['document'])
def save_file(message):
    clear_foulder()
    file = bot.get_file(message.document.file_id)
    dt_ufa = datetime.utcnow() + timedelta(hours=5)
    path = './saves/' + dt_ufa.strftime('NewYearParty-%d%m%y-%H%M.savegame')
    download = bot.download_file(file.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(download)
        
    bot.send_message(message.chat.id, 'Я добавил твоё последнее сохранение. Передай ребятам, что закинул файл мне :)')
    
@bot.message_handler(commands=['last'])
def get_save(message):
    onlyfiles = [f for f in listdir('/home/imtoopunkforyou/prog/astro/saves') if isfile(join('/home/imtoopunkforyou/prog/astro/saves', f))]
    file = open(f'./saves/{onlyfiles[0]}', 'rb')
    bot.send_document(message.chat.id, file)

if __name__ == '__main__':
    bot.polling(non_stop=True)