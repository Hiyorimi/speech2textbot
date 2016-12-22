## Speech2Text telegram bot (via telepot) v.2.0

This is light demo of [telepot](https://github.com/nickoala/telepot) and telegram capabilities to improve your life a bit. You can run this bot and recognize annoying audio messages to text if you dislike them or simply can't listen right away.

## Demo 

You can try [@sp2txt_bot](https://telegram.me/sp2txt_bot) yourself. Just record a voice message, or forward one and wait couple of seconds.

## Installation

1. Get your Yandex.SpeechKit API key at [Yandex Developer Center](https://developer.tech.yandex.ru). Paste it inside 
2. Make sure [Bot Father](https://telegram.me/BotFather) approves of your intentation to create another bot. If so, get a token.
3. Install dependencies required for audio processing. Telegram uses OPUS for encoding voice messages, so:

```
$ sudo apt-get update && apt-get install libopus0 libopus-dev opus-tools # vorbis-tools
# if you are ok with some extra packages, you can try installing audiotools as a package
# or, for Mac
$ brew install opus-tools # vorbis-tools
```

Installation tested on Debian Wheezy. If you have troubles with opus-tools, check out notes below.

4. Install dependancies and run bot with:

```
$ git clone https://github.com/Hiyorimi/speech2textbot.git
$ cd speech2textbot && mkdir downloads
$ sed -i "s/SPEECH_KIT_API\ \=\ ''/SPEECH_KIT_API\ \=\ 'your-yandex-speech-kit-api-here'/g" speech2textbot.py
$ mkvirtualenv speech2textbot
(speech2textbot)$ pip install -r requirements.txt
```


On Mac you should add \'\' after -i:

```
$ sed -i '' "s/\=\ ''/\=\ 'your-yandex-speech-kit-api-here'/g" speech2textbot.py
```

## Running 

```
(speech2textbot)$ python speech2textbot.py [your token] 
```

## Final

I would be grateful for any ideas for improvement, feel free to fork, copy and modify.


## OPUS installation

If you can't build audiotools and fail to install opus-tools and opusfile from packages, you might want to build OPUS from [source](http://www.opus-codec.org/downloads/).

Since there is no installation guide, some tips. First of all, install system libs:

```
$ apt-get install vorbis-tools libogg-dev  libmpg123 libmp3lame-dev libmp3lame0 ffmpeg
```

1. Get opus, opus-tools and opusfile archives, unpack them with tar -xzf [file] 
2. cd into directory and run

```
$ ./configure
$ ./make
$ ./make install
```

You might need to install additional dependencies.
