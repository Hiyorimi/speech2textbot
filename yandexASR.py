# -*- coding: utf-8 -*-
import sys
import asyncio
import pprint
from xml.dom.minidom import parseString
import requests
import random
import os
from os.path import join, dirname

async def yadexASR(SPEECH_KIT_API_KEY, uuid, filename, topic='notes'):
        """
        Get's filename as an input and performs POST request to API, according to
        docs: https://tech.yandex.ru/speechkit/cloud/doc/dg/concepts/speechkit-dg-recogn-docpage/
        """

        uuid = ''.join(c for c in uuid if c in '1234567890abcdef')
        while (len(uuid)<32):
            uuid=uuid+random.choice('1234567890abcdef')
        # Link from docs
        url = 'https://asr.yandex.net/asr_xml?uuid=%s&key=%s&topic=%s&lang=ru-RU' % (uuid, SPEECH_KIT_API_KEY, topic)
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
        if response.status_code != 200:
            return None
        xml = parseString(response.text.encode('utf-8'))
        # There are several variants, we pick first — usually most precise
        var = xml.getElementsByTagName('variant')
        result=var[0].childNodes[0].nodeValue
        return result