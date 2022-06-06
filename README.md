# TGYTDL Bot

A simple, straightforward bot that downloads YouTube videos ( as video or audio only files ) via [pytube](https://github.com/pytube/pytube)<br>
You can find its running instance on [Telegram](https://telegram.me/DlFromYT_bot)

# Commands

* `/ytvid VIDEO_URL or reply to a message with URL` : <i>Downloads YouTube videos from URL</i>

* `/ytaud VIDEO_URL or reply to a message with URL` : <i>Downloads YouTube videos as audio from URL</i>

* `/ping` : <i>Gets bot response time</i>

# Dependencies

* [pyrogram](https://github.com/pyrogram/pyrogram)

* [TGCrypto](https://github.com/pyrogram/tgcrypto)

* [pytube](https://github.com/pytube/pytube)

* [psutil](https://github.com/giampaolo/psutil)

# Deploy

* <b>Railway</b>

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/bA1yuY?referralCode=6B3Q1r)

* <b>Heroku</b>

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/greplix/tgytdl)

* <b>Locally</b>

You need to edit `vars.py`. Set `NON_LOCAL` to `False` and supply the values in the `else` block.

>Docker

```
git clone https://github.com/greplix/tgytdl.git
cd tgytdl
docker build . -t tgytdl
docker run tgytdl
```

>Without Docker

```
git clone https://github.com/greplix/tgytdl.git
cd tgytdl
pip3 install -r requirements.txt
python3 bot.py
```
