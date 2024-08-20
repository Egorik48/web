import os

import telebot
from pydub import AudioSegment
from pytubefix import YouTube
from pytubefix.cli import on_progress
from telebot import types

from main_two import rate_us_dollar # импортируем курс доллара из папки main_two

bot = telebot.TeleBot('TOKEN') # Создаём бота
TOKEN = 'TOKEN'


def speech(): # Включается функция, если пользователь выбрал транскрибацию
    @bot.message_handler(commands=['voice'])
    def start(message):
        bot.send_message(message.from_user.id, 'Привет, это бот, который понимает ваш голос!'
                                               '\nСкажи что-нибудь или отправь')

    @bot.message_handler(content_types=['voice', 'audio', 'document'])
    def voice_processing(message):
        global AUDIO_FILE, file_info
        if message.content_type == 'voice': # если пользователь отправляет голосовое
            file_info = bot.get_file(message.voice.file_id) # получаем значения файла и скачиваем его
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'someone.ogg', 'wb') as f:
                f.write(downloaded_file)
                f.close()
            audio = AudioSegment.from_file("someone.ogg", format="ogg")

            audio.export(f'{file_info.file_path[6:-4]}.flac', format="flac") # переводим формат ogg в flac

            AUDIO_FILE = f"C://Users//user//Desktop//pythonProject//pythonProjectlast//{file_info.file_path[6:-4]}.flac"
        elif message.content_type == 'audio': # если пользователь отправляет аудио
            file_info = bot.get_file(message.audio.file_id) # получаем значения файла и скачиваем его в ЛЮБОМ ФОРМАТЕ
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'someone.{file_info.file_path[-3:]}', 'wb') as f:
                f.write(downloaded_file)
                f.close()
            audio = AudioSegment.from_file(f"someone.{file_info.file_path[-3:]}", format=f"{file_info.file_path[-3:]}")

            audio.export(f'{file_info.file_path[6:-4]}.flac', format="flac")# переводим формат в flac

            AUDIO_FILE = f"C://Users//user//Desktop//pythonProject//pythonProjectlast//{file_info.file_path[6:-4]}.flac"
        elif message.content_type == 'document': # аналогично с документом
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'someone.{file_info.file_path[-3:]}', 'wb') as f:
                f.write(downloaded_file)
                f.close()
            audio = AudioSegment.from_file(f"someone.{file_info.file_path[-3:]}", format=f"{file_info.file_path[-3:]}")

            audio.export(f'{file_info.file_path[10:-4]}.flac', format="flac")

            AUDIO_FILE = f"C://Users//user//Desktop//pythonProject//pythonProjectlast//{file_info.file_path[10:-4]}.flac" # путь файла
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)

            try:
                text = r.recognize_google(audio, language='ru-RU').capitalize() # распознаем речь 
            except sr.UnknownValueError:
                bot.send_message(message.from_user.id, "Не понимаю, что ты сказал? /voice")

            except sr.RequestError as e:
                bot.send_message(message.from_user.id, "Бот не вывез, ошибка: {0}".format(e))
                speech()
        from gigachat import GigaChat # используем нейросеть для постановления пунктуации 

        # Используйте токен, полученный в личном кабинете из поля Авторизационные данные
        try:
            with GigaChat(credentials='NDdmNmE5NDItNDYwOC00NTU5LWI5ZWQtNDgzZDU0ZDU1ND'
                                      'U4OjJmYmRhYzk0LThlNjMtNDQ3Ny1iNWNlLTk4NTkwMTQxYjYwNg==',
                          verify_ssl_certs=False) as giga:
                response = giga.chat(f'У меня есть такой текст: "{text}"'
                                     f', исправь пунктуацию и выводи мне ТОЛЬКО ИСПРАВЛЕННЫЙ ТЕКСТ')
                bot.send_message(message.from_user.id, f'<b>Вы сказали</b>: \n{response.choices[0].message.content}'
                                                       f'\n\nЧтобы продолжить: скиньте ещё аудио или /start', parse_mode='html')
        except Exception:
            bot.send_message(message.from_user.id, 'Похоже нечего обрабатывать, что-то пошло не по плану /voice')
        os.remove(AUDIO_FILE)



# Определение функции для скачивания видео с YouTube
def download():
    # Обработчик сообщений с командой 'YouTube'
    @bot.message_handler(commands=['YouTube'])
    def response(function_continuation):
        # Сообщение пользователю с просьбой прислать ссылку на видео
        second_mess = ("Отлично! Пришли ссылку/ссылки видео на youtube!"
                       "\n<b>Важно!</b> <i>если ты кидаешь ссылкИ, то кидай их через пробел</i>. Это очень важно!")

        # Отправка сообщения пользователю
        bot.send_message(function_continuation.chat.id, second_mess, parse_mode='html')

    # Обработчик сообщений с текстом или видео
    @bot.message_handler(content_types=['text', 'video'])
    def handle_video(message):
        if message.text:
            # Объявление переменной для хранения экземпляра YouTube
            yt = None
            # Цикл для обработки каждой ссылки в сообщении пользователя
            for url in message.text.split(' '):
                try:
                    # Создание экземпляра YouTube с ссылкой и обработчиком прогресса
                    yt = YouTube(url, on_progress_callback=on_progress)
                    # Получение потока с самым высоким разрешением
    ys = yt.streams.get_highest_resolution()
                    # Сообщение пользователю о начале загрузки
                    bot.send_message(chat_id=message.chat.id, text='Ждем всем селом, пока загрузятся видосики')
                    # Скачивание видео
                    ys.download()
                except Exception as e:
                    # Вывод ошибки в консоль
                    print(f'Ooops: {e}')
            # Отправка скачанного видео пользователю
            bot.send_video(chat_id=message.chat.id, video=open(f'{yt.title}.mp4', 'rb'))
            # Удаление файла после отправки
            os.remove(f'{yt.title}.mp4')
        # Сообщение пользователю после завершения операции
        bot.send_message(chat_id=message.chat.id, text='Используй с удовольствием:), /start')

# Обработчик команды 'start'
@bot.message_handler(commands=['start'])
def startBot(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    space = ' '

    if first_name is None:
        first_name = ''
        space = ''
    elif last_name is None:
        last_name = ''
        space = ''

    first_mess = (f"<b>{first_name}{space + last_name}</b>, привет!\nЭто телеграмм бот,"
                  f" в котором ты можешь <b>скачать видео с youtube</b>!"
                  f"\nТак же существует функция распознавания <b>голоса в текст</b>!"
                  f"\nВыбирай ")
    # Создание клавиатуры с двумя кнопками
    markup = types.InlineKeyboardMarkup()
    button_youtube = types.InlineKeyboardButton(text='Скачивать видео 🔄', callback_data='download')
    button_voice = types.InlineKeyboardButton(text='Голос в текст 🔊', callback_data='talk')
    markup.add(button_youtube, button_voice)
    # Отправка сообщения пользователю с приветствием и клавиатурой
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

# Обработчик обратных вызовов для кнопок 'download' и 'talk'
@bot.callback_query_handler(func=lambda call: call.data == 'download' or call.data == 'talk')
def advertisement(function_call):
    message = (f"<i>Интересный факт!</i>\n"
               f"На данный момент в сайте Банка России, <b>текущим курсом доллара</b>\n"
               f"является значение: <b>{rate_us_dollar}</b>, знай это\n"
               f"<s>здесь могла быть твоя реклама https://www.donationalerts.com/r/egor456544</s>")

    # Отправка сообщения пользователю с фактом и рекламой
    bot.send_message(function_call.message.chat.id, message, parse_mode='html')

    if function_call.data == 'talk':
        # Сообщение пользователю о необходимости отправить команду '/voice'
        bot.send_message(function_call.message.chat.id, 'Напиши /voice', parse_mode='html')
        # Вызов функции для распознавания голоса
        speech()
    elif function_call.data == 'download':
        # Сообщение пользователю о необходимости отправить команду '/YouTube'
        bot.send_message(function_call.message.chat.id, 'Напиши /YouTube', parse_mode='html')
        # Вызов функции для скачивания видео
        download()

bot.polling(none_stop=True, interval=0)
