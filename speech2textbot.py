# -*- coding: utf-8 -*-
import sys
import time
import telepot
import asyncio
import telepot.async
import pprint
from xml.dom.minidom import parseString
import requests
from pydub import AudioSegment
import random
import os

SPEECH_KIT_API = 'efe49eed-0ce0-4482-8c14-0cf141204bd9'
DOWNLOADS_DIR_NAME = 'downloads/'

class Speech2TextBot(telepot.async.Bot):
    def __init__(self, *args, **kwargs):
        super(Speech2TextBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.async.helper.Answerer(self)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Chat Message:', content_type, chat_type, chat_id)
        if content_type == 'voice':
            pprint.pprint(msg)
            if ( msg['voice']['file_size']< 1033896):
                bot.download_file(msg['voice']['file_id'], DOWNLOADS_DIR_NAME + msg['voice']['file_id'])
                answer = self._get_text_from_telegram_voice_file( DOWNLOADS_DIR_NAME + msg['voice']['file_id'])
                os.remove(DOWNLOADS_DIR_NAME + msg['voice']['file_id'])
                bot.sendMessage(chat_id, answer)
            else:
                bot.sendMessage(chat_id, 'Слишком длинное аудиосообщение, извини. \
                    Попробуй отправить запись короче.')

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        def compute_answer():
            articles = [{'type': 'article',
                            'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self._answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)

    def _get_text_from_telegram_voice_file (self, filename):
        converted = AudioSegment.from_ogg(filename)
        converted.export(filename+'.mp3')
        text = self._yadexASR(filename[:-30:-1], filename = filename+'.mp3')
        os.remove(filename+'.mp3')
        return text

    def _yadexASR(self, uuid, filename, key=SPEECH_KIT_API, topic='notes'):
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
        response = requests.post(url, files={'audio' :audio}, headers=headers)
        print (response.text)
        xml = parseString(response.text.encode('utf-8'))
        # There are several variants, we pick first — usually most precise
        var = xml.getElementsByTagName('variant')
        result=var[0].childNodes[0].nodeValue
        return result


TOKEN = sys.argv[1]  # get token from command-line

if (SPEECH_KIT_API != ''):

    bot = Speech2TextBot(TOKEN)
    loop = asyncio.get_event_loop()

    loop.create_task(bot.message_loop())
    print('Listening ...')

    loop.run_forever()

else:

    print ('Please regester your Yandex Speech Kit API Key at \
https://developer.tech.yandex.ru and paste it into SPEECH_KIT_API')

