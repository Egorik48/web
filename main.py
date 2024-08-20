import os

import telebot
from pydub import AudioSegment
from pytubefix import YouTube
from pytubefix.cli import on_progress
from telebot import types

from main_two import rate_us_dollar

bot = telebot.TeleBot('6675946515:AAEr3ILWaVU3tRjlVSErphh7wuCmqZ8slcU')
TOKEN = '6675946515:AAEr3ILWaVU3tRjlVSErphh7wuCmqZ8slcU'


def speech():
    @bot.message_handler(commands=['voice'])
    def start(message):
        bot.send_message(message.from_user.id, 'Привет, это бот, который понимает ваш голос!'
                                               '\nСкажи что-нибудь или отправь')

    @bot.message_handler(content_types=['voice', 'audio', 'document'])
    def voice_processing(message):
        global AUDIO_FILE, file_info
        if message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'someone.ogg', 'wb') as f:
                f.write(downloaded_file)
                f.close()
            audio = AudioSegment.from_file("someone.ogg", format="ogg")

            audio.export(f'{file_info.file_path[6:-4]}.flac', format="flac")

            AUDIO_FILE = f"C://Users//user//Desktop//pythonProject//pythonProjectlast//{file_info.file_path[6:-4]}.flac"
        elif message.content_type == 'audio':
            file_info = bot.get_file(message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'someone.{file_info.file_path[-3:]}', 'wb') as f:
                f.write(downloaded_file)
                f.close()
            audio = AudioSegment.from_file(f"someone.{file_info.file_path[-3:]}", format=f"{file_info.file_path[-3:]}")

            audio.export(f'{file_info.file_path[6:-4]}.flac', format="flac")

            AUDIO_FILE = f"C://Users//user//Desktop//pythonProject//pythonProjectlast//{file_info.file_path[6:-4]}.flac"
        elif message.content_type == 'document':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'someone.{file_info.file_path[-3:]}', 'wb') as f:
                f.write(downloaded_file)
                f.close()
            audio = AudioSegment.from_file(f"someone.{file_info.file_path[-3:]}", format=f"{file_info.file_path[-3:]}")

            audio.export(f'{file_info.file_path[10:-4]}.flac', format="flac")

            AUDIO_FILE = f"C://Users//user//Desktop//pythonProject//pythonProjectlast//{file_info.file_path[10:-4]}.flac"
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
            #audio = r.record(source)  # read the entire audio file

            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                text = r.recognize_google(audio, language='ru-RU').capitalize()
                print(text)
            except sr.UnknownValueError:
                bot.send_message(message.from_user.id, "Не понимаю, что ты сказал? /voice")

            except sr.RequestError as e:
                bot.send_message(message.from_user.id, "Бот не вывез, ошибка: {0}".format(e))
                speech()
        from gigachat import GigaChat

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


def download():
    @bot.message_handler(commands=['YouTube'])
    def response(function_continuation):
        second_mess = ("Отлично! Пришли ссылку/ссылки видео на youtube!"
                       "\n<b>Важно!</b> <i>если ты кидаешь ссылкИ, то кидай их через пробел</i>. Это очень важно!")

        bot.send_message(function_continuation.chat.id, second_mess, parse_mode='html')

    @bot.message_handler(content_types=['text', 'video'])
    def handle_video(message):
        if message.text:
            yt = None  # Объявляем переменную yt вне цикла
            for url in message.text.split(' '):
                try:
                    yt = YouTube(url, on_progress_callback=on_progress)
                    ys = yt.streams.get_highest_resolution()
                    bot.send_message(chat_id=message.chat.id, text='Ждем всем селом, пока загрузятся видосики')
                    ys.download()
                except Exception as e:
                    print(f'Ooops: {e}')
            bot.send_video(chat_id=message.chat.id, video=open(f'{yt.title}.mp4', 'rb'))
            os.remove(f'{yt.title}.mp4')
        bot.send_message(chat_id=message.chat.id, text='Используй с удовольствием:), /start')


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
    markup = types.InlineKeyboardMarkup()
    button_youtube = types.InlineKeyboardButton(text='Скачивать видео 🔄', callback_data='download')
    button_voice = types.InlineKeyboardButton(text='Голос в текст 🔊', callback_data='talk')
    markup.add(button_youtube, button_voice)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'download' or call.data == 'talk')
def advertisement(function_call):
    message = (f"<i>Интересный факт!</i>\n"
               f"На данный момент в сайте Банка России, <b>текущим курсом доллара</b>\n"
               f"является значение: <b>{rate_us_dollar}</b>, знай это\n"
               f"<s>здесь могла быть твоя реклама https://www.donationalerts.com/r/egor456544</s>")

    bot.send_message(function_call.message.chat.id, message, parse_mode='html')

    if function_call.data == 'talk':
        bot.send_message(function_call.message.chat.id, 'Напиши /voice', parse_mode='html')
        speech()
    elif function_call.data == 'download':
        bot.send_message(function_call.message.chat.id, 'Напиши /YouTube', parse_mode='html')
        download()


bot.polling(none_stop=True, interval=0)
