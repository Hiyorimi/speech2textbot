# -*- coding: utf-8 -*-
import sys
import asyncio
from telepot import message_identifier, glance
import telepot.aio
import telepot.aio.helper
from telepot.aio.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
import pprint
from xml.dom.minidom import parseString
import requests
from pydub import AudioSegment
import random
import os

SPEECH_KIT_API = ''
DOWNLOADS_DIR_NAME = 'downloads/'

class Speech2TextBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Speech2TextBot, self).__init__(*args, **kwargs)


    async def _get_text_from_telegram_voice_file (self, filename):
        converted = AudioSegment.from_ogg(filename)
        converted.export(filename+'.mp3', format="mp3")
        text = await self._yadexASR(filename[:-30:-1], filename=filename+'.mp3')
        os.remove(filename+'.mp3')
        return text

    async def _yadexASR(self, uuid, filename, key=SPEECH_KIT_API, topic='notes'):
        """
        Get's filename as an input and performs POST request to API, according to
        docs: https://tech.yandex.ru/speechkit/cloud/doc/dg/concepts/speechkit-dg-recogn-docpage/
        """

        uuid = ''.join(c for c in uuid if c in '1234567890abcdef')
        while (len(uuid)<32):
            uuid=uuid+random.choice('1234567890abcdef')
        print (uuid)
        # Link from docs
        url = 'https://asr.yandex.net/asr_xml?uuid=%s&key=%s&topic=%s&lang=ru-RU' % (uuid, key, topic)
        # Binary mode, cause it required to send as multipart
        audio = open(filename,'rb')
        # x-mpeg-3 is not recommended, but it is most common codec
        headers={'Content-Type': 'audio/x-mpeg-3'}

        #Async magic
        loop = asyncio.get_event_loop()
        def _do_request():
            return requests.post(url, files={'audio' :audio}, headers=headers)
        future = loop.run_in_executor(None, _do_request)
        response = await future
        print (response.text)
        xml = parseString(response.text.encode('utf-8'))
        # There are several variants, we pick first — usually most precise
        var = xml.getElementsByTagName('variant')
        result=var[0].childNodes[0].nodeValue
        return result

    async def _serve_answer(self, chat_id, msg):
        await bot.download_file(msg['voice']['file_id'], DOWNLOADS_DIR_NAME + msg['voice']['file_id'])
        answer = await self._get_text_from_telegram_voice_file( DOWNLOADS_DIR_NAME + msg['voice']['file_id'])
        os.remove(DOWNLOADS_DIR_NAME + msg['voice']['file_id'])
        await bot.sendMessage(chat_id, answer)
        return


    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = glance(msg)
        print('Chat Message:', content_type, chat_type, chat_id)
        if content_type == 'voice':
            pprint.pprint(msg)
            if ( msg['voice']['file_size']< 1033896):
                await self._serve_answer(chat_id, msg)
            else:
                await bot.sendMessage(chat_id, 'Слишком длинное аудиосообщение, извини. \
                    Попробуй отправить запись короче.')

    async def on__idle(self, event):
        await self.sender.sendMessage('Окей, если что, пересылай сообщения или кидай войсики. Я тут.')
        self.close()


TOKEN = sys.argv[1]  # get token from command-line


if (SPEECH_KIT_API != ''):

    bot = telepot.aio.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, Speech2TextBot, timeout=40),
    ])

    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop())
    print('Listening ...')

    loop.run_forever()

else:

    print ('Please regester your Yandex Speech Kit API Key at \
https://developer.tech.yandex.ru and paste it into SPEECH_KIT_API')