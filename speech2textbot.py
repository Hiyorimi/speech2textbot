# -*- coding: utf-8 -*-
import os
import sys
import time
import asyncio
import pprint
import requests
import random
import logging

from telethon import TelegramClient, events
from pydub import AudioSegment
from xml.dom.minidom import parseString
from os.path import join, dirname
from dotenv import load_dotenv
from collections import defaultdict
from yandexASR import yadexASR


logging.basicConfig(level=logging.WARNING)
SPEECH_KIT_API_KEY = ''
DOWNLOADS_DIR_NAME = './downloads/'
# "When did we last react?" dictionary, 0.0 by default
recent_reacts = defaultdict(float)

def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


async def get_text_from_telegram_voice_file (filename, filetype = 'voice'):
    if filetype == 'voice':
        converted = AudioSegment.from_ogg(filename)
    if filetype == 'audio':
        converted = AudioSegment.from_mp3(filename)
    converted.export(filename+'.mp3', format="mp3")
    text = await yadexASR(SPEECH_KIT_API_KEY, filename[:-30:-1], filename=filename+'.mp3')
    os.remove(filename+'.mp3')
    return text


async def serve_answer(filename, filetype = 'voice'):
    answer = await get_text_from_telegram_voice_file(filename, filetype)
    os.remove(filename)
    return answer



def can_react(chat_id):
    # Get the time when we last sent a reaction (or 0)
    last = recent_reacts[chat_id]

    # Get the current time
    now = time.time()

    # If 10 minutes as seconds have passed, we can react
    if now - last < 10 * 60:
        # Make sure we updated the last reaction time
        recent_reacts[chat_id] = now
        return True
    else:
        return True

def is_new_client(chat_id):
    # Get the time when we last sent a reaction (or 0)
    last = recent_reacts[chat_id]

    return last == 0.0

# Register `events.NewMessage` before defining the client.
# Once you have a client, `add_event_handler` will use this event.
@events.register(events.NewMessage)
async def handler(event):
    if event.raw_text != '':
        if 'shrug' in event.raw_text:
            if can_react(event.chat_id):
                await event.respond(r'¯\_(ツ)_/¯')
        elif '/help' in event.raw_text:
            github_url = 'https://github.com/Hiyorimi/speech2textbot'
            await event.respond("""👾Я распознаю речь в отправленных мне голосовых сообщениях или \
    аудиофайлах и отвечаю на них текстом. Можешь не париться, если ты на совещании или паре, а просто пересылать все \
    сообщения мне. Я понимаю команды:

    /help — Доступные команды и помощь в использовании бота.

    Если бот тебе помог, то просто расскажи о нём своим друзьям.

    Этот проект имеет открытый исходный код и ты можешь запустить свою версию: """ + github_url)
        else:
            await event.respond("""Unfortunately, now you can use only /help command.""")
    else:
        # We can also use client methods from here
        client = event.client
        if event.message is not None:
            file_shorcut = None
            if event.message.voice is not None:
                filetype = 'voice'
                file_shorcut = event.message.voice
            elif event.message.audio is not None:
                filetype = 'audio'
                file_shorcut = event.message.audio

            if file_shorcut is not None:
                if (file_shorcut.size < 1033896):
                    client = event.client
                    filename = await client.download_media(event.message, DOWNLOADS_DIR_NAME)
                    answer = await serve_answer(filename, filetype)
                    if answer != None:
                        await event.respond(answer)
                    else:
                        await event.respond("😕 что-то пошло не так, извините.")
                else:
                    await event.respond('Слишком длинное аудиосообщение, извини. \
                        Попробуй отправить запись короче.')




dotenv_path = join(dirname(__file__), '.env')
if (load_dotenv(dotenv_path)):
    SPEECH_KIT_API_KEY = os.environ.get("SPEECH_KIT_API_KEY")
    DEBUG = os.environ.get("DEBUG")
else:
    SPEECH_KIT_API_KEY = sys.argv[1]  # get token from command-line

if ((SPEECH_KIT_API_KEY != '') and (SPEECH_KIT_API_KEY)):
    # Telethon

    client = TelegramClient(
        os.environ.get('TG_SESSION', 'replier'),
        get_env('TG_API_ID', 'Enter your API ID: ', int),
        get_env('TG_API_HASH', 'Enter your API hash: '),
        proxy=None
    )

    with client:
        # This remembers the events.NewMessage we registered before
        client.add_event_handler(handler)

        print('(Press Ctrl+C to stop this)')
        client.run_until_disconnected()

else:

    print ('Please regester your Yandex Speech Kit API Key at \
    https://developer.tech.yandex.ru and paste it into SPEECH_KIT_API_KEY \
           python or .env variable.')
