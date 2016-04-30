## Speech2Text telegram bot (via telepot) 

This is light demo of [telepot](https://github.com/nickoala/telepot) and telegram capabilities to improve your life a bit. You can run this bot and recognize annoying audio messages to text if you dislike them or simply can't listen right away.

## Demo 

You can try [@sp2txt_bot](https://telegram.me/sp2txt_bot) yourself. Just record a voice message, or forward one and wait couple of seconds.

## Installation

1. Get your Yandex.SpeechKit API key at [Yandex Developer Center](https://developer.tech.yandex.ru). Paste it inside 
2. Make sure [Bot Father](https://telegram.me/BotFather) approves of your intentation to create another bot. If so, get a token.
3. Run your bot with

```
$ mkdir downloads
$ git clone https://github.com/Hiyorimi/speech2textbot.git
$ mkvirtualenv speech2textbot
(speech2textbot)$ pip install -r requirements.txt
```

## Running 

```
(speech2textbot)$ python speech2textbot.py [your token] 
```

## Final

I would be grateful for any ideas for improvement, feel free to fork, copy and modify.
