from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from pyrogram import Client, filters,idle
import re
import logging,datetime
from vars import *
from core.functions import *
logging.basicConfig(level=logging.INFO)

bot_token = BOT_TOKEN
api_id = API_ID
api_hash = API_HASH
log_group = LOG_GRP_ID

REGEX = re.compile(r'https?://(\S+\.)?\S+\.?be(\.\S+)?/(w\S+|s\S+/)?-?(\?v=)?\w+')

ytbot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)
logging.info('CREATED BOT CLIENT')


@ytbot.on_message(
    filters.command("start") &
    ~filters.edited
)
async def strt(_: Client,m: Message):
    await m.reply_text(WELCOME,
    parse_mode='markdown',
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Repo',url='https://github.com/greplix/tgytdl'),
        InlineKeyboardButton('Dev',url='https://github.com/greplix')]
    ]))

@ytbot.on_message(
    filters.command('help') &
    ~filters.edited
)
async def hel(_: Client, m: Message):
    await m.reply_text(text=HELP, parse_mode='markdown')

@ytbot.on_message(
    filters.command('ytvid') &
    ~filters.edited
)
async def ytv(client: Client, m: Message):
    if m.reply_to_message:
        reg = REGEX.search(m.reply_to_message.text.strip())
        if not reg:
            return await m.reply_text('Didn\'t find a video URL from the message')
        link = reg.group()
    else:
        if len(m.command) != 2:
            return await m.reply_text(text='Reply to a message with URL or provide a link')
        link = m.command[1].strip()
        if not REGEX.search(link):
            return await m.reply_text('Invalid video URL')
    try:
        s = await m.reply_text('**Fetching information...**',parse_mode='md')
        ytobj,streams = get_streams(link,'video')
    except Exception as e:
        await s.edit_text(f'**Exception**: `{e}`',parse_mode='markdown');return
    keyboard = genkeyboard(streams,link,'video')
    await m.reply_photo(
        photo=ytobj.thumbnail_url,
        caption=f'**Title:** {ytobj.title}\n**Author:** {ytobj.author}',
        reply_markup=keyboard
    )
    await s.delete()

@ytbot.on_callback_query()
async def respond_vid(client,callback: CallbackQuery):
    splitted = callback.data.split('|')
    link,itag=str(splitted[0]),int(splitted[1])
    try:await dvid(client,link,itag,callback)
    except Exception as e:
        await callback.edit_message_text(f'**Exception:** `{e}`','md')

@ytbot.on_message(
    filters.command('ytaud') &
    ~filters.edited
)
async def yta(client: Client, m: Message):
    if m.reply_to_message:
        reg = REGEX.search(m.reply_to_message.text.strip())
        if not reg:
            return await m.reply_text('Didn\'t find a video URL from the message')
        link = reg.group()
    else:
        if len(m.command) != 2:
            return await m.reply_text(text='Reply to a message with URL or provide a link')
        link = m.command[1].strip()
        if not REGEX.search(link):
            return await m.reply_text('Invalid video URL')
    try:
        s = await m.reply_text('**Fetching information...**',parse_mode='md')
        ytobj,streams = get_streams(link,'audio')
    except Exception as e:
        await s.edit_text(f'**Exception**: `{e}`',parse_mode='markdown');return
    keyboard = genkeyboard(streams,link,'audio')
    await m.reply_photo(
        photo=ytobj.thumbnail_url,
        caption=f'**Title:** {ytobj.title}\n\n**Choose a download filesize-**',
        reply_markup=keyboard
    )
    await s.delete()

@ytbot.on_message(
    filters.command('ping') &
    ~filters.edited
)
async def pong(c,m: Message):
    now = datetime.datetime.now()
    meh = await m.reply_text('Pong!')
    then = datetime.datetime.now()
    import time;time.sleep(0.5)
    delta = round(((then - now).microseconds)/1000, 1)
    await meh.edit_text(f'Pong: {delta}ms')


ytbot.start()
try:
    ytbot.send_message(
    chat_id=log_group,
    text=f'''
**Bot has been Deployed**
'''+sys_info(),
    parse_mode='markdown'
    )
except:pass
idle()
