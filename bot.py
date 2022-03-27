import os,psutil
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from pyrogram import Client, filters
from pytube import YouTube
import subprocess,logging,os,datetime

logging.basicConfig(level=logging.INFO)

bot_token = str(os.environ.get('BOT_TOKEN'))
api_id = int(os.environ.get('API_ID'))
api_hash = str(os.environ.get('API_HASH'))
try:log_group = int(os.environ.get('LOG_GRP_ID'))
except:log_group = 0

streams_dict = {}

def sys_info():
    t1,t2,t3 = psutil.getloadavg()
    cc = os.cpu_count()
    cu = psutil.cpu_percent()
    r = psutil.virtual_memory()[2]
    msg = f'''
**Task Avg**: `{t1} {t2} {t3}`
**CPU Usage**: `{cu}%`
**CPUs**: `{cc}`
**RAM Usage**: `{r}%`
    '''
    return msg

def get_streams(link):
    rs = []
    rd = {}
    p = YouTube(link)
    thumb = p.thumbnail_url
    title = p.title
    author = p.author
    streams = p.streams.filter(type='video',progressive=True)
    for x in streams:
        rs.append((x.itag,x.resolution))
    if list(streams_dict.keys()) == []:key=0
    else:key=list(streams_dict.keys())[-1] + 1
    streams_dict[key]=streams
    rd['key']=key
    rd['thumb']=thumb
    rd['title']=title
    rd['author']=author
    rd['streams']=rs
    return rd


async def progress(current,total,c: Client,mid,cid):
    t=round((current*100/total),1)
    if t % 20 == 0.0:
        bar = "█"*int(t/10)
        space = " "*int(10-(t/10))
        cmbs = round((current/10**6),2);tmbs = round((total/10**6),2)
        try:await c.edit_message_text(chat_id=cid,message_id=mid,text=f'''
**Uploading...**
`|{bar}{space}|` **{t}%**

**{cmbs}/{tmbs} MB**
''')
        except:pass
    else:pass


async def dvid(client: Client,key,itag,callback: CallbackQuery):
    import secrets
    filename = f'{secrets.token_hex(16)}.mp4'
    a=await callback.edit_message_text(text=f'**Downloading...**',parse_mode='markdown')
    streams = streams_dict[key]
    vid  =streams.get_by_itag(itag)
    logging.info(f'STREAM {itag} FETCHED')
    vid.download(output_path='videos/',filename=filename)
    logging.info('DOWNLOADED VIDEO')
    try:
        await client.send_video(
            chat_id=a.chat.id,
            video=f'videos/{filename}',
            caption=f'**Title:** {str(vid.title)}\n**Resolution:** {vid.resolution}',
            supports_streaming=True,
            progress=progress,
            progress_args=(client,a.message_id,a.chat.id)
        )
        os.remove(f'videos/{filename}')
        logging.info('VIDEO LOCALLY REMOVED')
    except:
        try:os.remove(f'videos/{filename}');logging.info('VIDEO LOCALLY REMOVED')
        except:pass
    await a.delete()

async def daud(client: Client,key,itag,callback: CallbackQuery):
    pass #TODO: add feature to download audio


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
    welcome = '''
Hi there, you can use me to download videos and audios from YouTube just by providing its link!

**Use /help for commands**

**Created By**: @greplix
        '''
    await m.reply_text(welcome,parse_mode='markdown')

@ytbot.on_message(
    filters.command('help') &
    ~filters.edited
)
async def hel(_: Client, m: Message):
    help = '''
**Usage**

/ytvid `VIDEO_LINK` : __Downloads videos from YouTube__

/ytaud `VIDEO_LINK`` : __Downloads videos as audio(Not functional yet)__

/ping : __Shows bot response time__

/help : __Display this message__
'''
    await m.reply_text(text=help, parse_mode='markdown')

@ytbot.on_message(
    filters.command('ytvid') &
    ~filters.edited
)
async def ytv(client: Client, m: Message):
    if m.reply_to_message:
        link = m.reply_to_message.text.strip()
        try:
            assert link.startswith('https://') or link.startswith('http://')
        except AssertionError:
            await m.reply_text(f'Reply to a message or provide link')
            return
    else:
        splitted = m.text.split(" ")
        if len(splitted) != 2:
            await m.reply_text(text='Reply to a message with URL or provide a link')
            return
        else:
            link = splitted[1].strip()
            try:
                assert link.startswith('https://') or link.startswith('http://')
            except AssertionError:
                await m.reply_text(f'Error in parsing URL');return
            except Exception as e:
                await m.reply_text(f'**Exception**: `{e}`',parse_mode='markdown');return
    try:
        s=await m.reply_text('**Fetching information...**',parse_mode='md')
        results = get_streams(link)
    except Exception as e:
        await s.edit_text(f'**Exception**: `{e}`',parse_mode='markdown');return
    kek = results['key']
    t=results['title'];tn=results['thumb']
    streams=results['streams']
    author=results['author']
    kb=[]
    while len(streams) != 0:
        lel=[]
        for x in streams[:3]:
            lel.append(InlineKeyboardButton(text=f'{x[1]}',callback_data=f'{kek}:{x[0]}'))
            streams.remove(x)
        kb.append(lel)
    keyboard = InlineKeyboardMarkup(kb)
    await m.reply_photo(
        photo=tn,
        caption=f'**Title:** {t}\n**Author:** {author}',
        reply_markup=keyboard
    )
    await s.delete()
@ytbot.on_callback_query(
    filters.regex('^.*')
)
async def respond_vid(client,callback: CallbackQuery):
    key=int(callback.data.split(':')[0])
    itag=int(callback.data.split(':')[1])
    try:
        await dvid(client,key,itag,callback)
    except Exception as e:
        await callback.edit_message_text(f'**Exception:** `{e}`','md')
    del streams_dict[key]

@ytbot.on_message(
    filters.command('ytaud') &
    ~filters.edited
)
async def yta(client: Client,m: Message):
    await m.reply_text('Coming soon...')

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

from pyrogram import idle
ytbot.start()
try:
    s = sys_info()
    ytbot.send_message(
        chat_id=log_group,
        text=f'''
**Bot has been Deployed**
'''+s,
        parse_mode='markdown'
    )
except Exception:
    pass
idle()
