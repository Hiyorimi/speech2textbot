# -*- coding: utf-8 -*-
import sys
import time
import telepot
import pprint
from xml.dom.minidom import parseString
import requests
import audiotools
import random
import os

SPEECH_KIT_API = ''

def yadexASR(uuid, filename, key=SPEECH_KIT_API, topic = 'notes'):
"""Get's filename as an input and performs POST request to API, according to
docs: https://tech.yandex.ru/speechkit/cloud/doc/dg/concepts/speechkit-dg-recogn-docpage/
"""
    uuid = ''.join(c for c in uuid if c in '1234567890abcdef')
    while (len(uuid)<32):
        uuid=uuid+random.choice('1234567890abcdef')
    print uuid
    # Link from docs
    url = 'https://asr.yandex.net/asr_xml?uuid=%s&key=%s&topic=%s&lang=ru-RU' % (uuid, key, topic)
    # Binary mode, cause it required to send as multipart
    audio = open(filename,'rb')
    # x-mpeg-3 is not recommended, but it is most common codec
    headers={'Content-Type': 'audio/x-mpeg-3'}
    response = requests.post(url, files={'audio' :audio}, headers=headers)
    print response.text
    xml = parseString(response.text.encode('utf-8'))
    # There are several variants, we pick first — usually most precise 
    var = xml.getElementsByTagName('variant')
    result=var[0].childNodes[0].nodeValue
    return result

def get_text_from_telegram_voice_file (filename):
    converted = audiotools.open(filename).convert( filename+'.mp3', audiotools.AVAILABLE_TYPES[1])
    text = yadexASR(filename[:-30:-1], filename = filename+'.mp3')
    os.remove(filename+'.mp3')
    return text

def handle(msg):
    flavor = telepot.flavor(msg)

    # chat message
    if flavor == 'chat':
        content_type, chat_type, chat_id = telepot.glance(msg)
        print ('Chat Message:', content_type, chat_type, chat_id)

        if content_type == 'voice':
            pprint.pprint(msg)
            if ( msg['voice']['file_size']< 1033896):
                bot.download_file(msg['voice']['file_id'], './download/'+msg['voice']['file_id'])
                answer = get_text_from_telegram_voice_file('./download/'+msg['voice']['file_id'])
                os.remove('./download/'+msg['voice']['file_id'])
                bot.sendMessage(chat_id, answer)
            else:
                bot.sendMessage(chat_id, 'Слишком длинное аудиосообщение, извини. \
                    Попробуй отправить запись короче.')



    # callback query - originated from a callback button
    elif flavor == 'callback_query':
        query_id, from_id, query_data = telepot.glance(msg, flavor=flavor)
        print ('Callback query:', query_id, from_id, query_data)

    # inline query - need `/setinline`
    elif flavor == 'inline_query':
        query_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
        print ('Inline Query:', query_id, from_id, query_string)

        # Compose your own answers
        articles = [{'type': 'article',
                        'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

        bot.answerInlineQuery(query_id, articles)

    # chosen inline result - need `/setinlinefeedback`
    elif flavor == 'chosen_inline_result':
        result_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
        print ('Chosen Inline Result:', result_id, from_id, query_string)

        # Remember the chosen answer to do better next time

    else:
        raise telepot.BadFlavor(msg)


TOKEN = sys.argv[1]  # get token from command-line

if (SPEECH_KIT_API != ''):

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle)
    print ('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)

else:

    print 'Please regester your Yandex Speech Kit API Key at \
https://developer.tech.yandex.ru and paste it into SPEECH_KIT_API'

