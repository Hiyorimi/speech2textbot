# Speech2Text telegram bot (via telepot)

This is light demo of [telepot](https://github.com/nickoala/telepot) and telegram capabilities
to improve your life a bit. You can run this bot and recognize annoying audio messages
to text if you dislike them or simply can't listen right away.

## Demo 

You can try [@sp2txt_bot](https://telegram.me/sp2txt_bot) yourself. Just record a voice message,
or forward one and wait couple of seconds.

## Installation

1. Get your Yandex.SpeechKit API key at [Yandex Developer Center](https://developer.tech.yandex.ru).  
2. Make sure [Bot Father](https://telegram.me/BotFather) approves your intentation to create another bot.
If so, get a token.
3. Install dependencies required for audio processing. Telegram uses OPUS for encoding voice messages, so:

```
$ sudo apt-get update && sudo apt-get install libopus0 libopus-dev opus-tools vorbis-tools libmp3lame-dev libogg-dev libogg0 libmp3lame0 
# if you are ok with some extra packages, you can try installing audiotools as a package
# or, for Mac
$ brew install opus-tools # vorbis-tools
```

Installation was tested on `Debian Wheezy` and `El Capitan`.
If you have troubles with opus-tools, check out notes below.

4. Install dependancies and run bot with:

```
$ mkvirtualenv speech2textbot
$ git clone https://github.com/tuffy/python-audio-tools.git && cd python-audio-tools.git
$ make install && cd ..
$ git clone https://github.com/Hiyorimi/speech2textbot.git
$ cd speech2textbot && mkdir downloads
(speech2textbot)$ pip install -r requirements.txt
```

## Running 

```
(speech2textbot)$ python speech2textbot.py [-h] [--token TOKEN] [--api-key API_KEY]
```

## Final

I would be grateful for any ideas for improvement, feel free to fork, copy and modify.


### Audio codecs installation

Here are some tips for installing libs for encoding ogg and mp3.
First of all, install system libs:

```
$ apt-get install vorbis-tools libogg-dev  libmpg1230 libmp3lame-dev libmp3lame0 
```

Also you can follow [these](https://github.com/tuffy/python-audio-tools/issues/36#issuecomment-55150118) issue and install:

```
sudo apt-get install mpg123 twolame libtwolame-dev
sudo apt-get install lame mp3gain libmp3lame-dev libmpg123-dev
sudo apt-get install vorbis-tools libvorbis-dev
sudo apt-get install opus-tools libopus-dev
```

#### Building OPUS 

If you can't build audiotools and fail to install opus-tools and opusfile from packages,
you might want to build OPUS from [source](http://www.opus-codec.org/downloads/).

Since there is no installation guide, some tips.

1. Get opus, opus-tools and opusfile archives, unpack them with `tar -xzf [file]`
2. `cd` into directory and run

```
$ ./configure
$ ./make
$ ./make install
```

You might need to install additional dependencies in the process.
