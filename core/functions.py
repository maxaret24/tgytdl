import psutil,os
from pyrogram import Client
from pyrogram.types import CallbackQuery
import logging,secrets
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pytube import YouTube


def rmfile(filename):
    try:
        os.remove(filename)
    except:pass

def get_streams(link,type):
    p = YouTube(link)
    if type == 'video':
        streams = p.streams.filter(type='video',progressive=True)
    else:
        streams = p.streams.filter(type='audio',mime_type='audio/webm')
    return p,streams



async def dvid(client: Client,link,itag,callback: CallbackQuery):
    a = await callback.edit_message_text(text=f'**Downloading...**',parse_mode='markdown')
    yt = YouTube(link)
    vid = yt.streams.get_by_itag(itag)
    n = secrets.token_hex(16)
    ext = 'mp4' if vid.type == 'video' else 'webm'
    filename = f'{n}.{ext}'
    logging.info(f'STREAM {itag} FETCHED')
    vid.download(output_path='videos/',filename=filename)
    logging.info('DOWNLOADED')
    try:
        if vid.type == 'video':
            await client.send_video(
            chat_id=a.chat.id,
            video=f'videos/{filename}',
            caption=f'**Title:** {vid.title}\n**Resolution:** {vid.resolution}',
            supports_streaming=True,
            progress=progress,
            progress_args=(client,a.message_id,a.chat.id),
            file_name=vid.title
            )
        else:
            os.rename(f"videos/{filename}",f"videos/{n}.mp3")
            await callback.edit_message_text(text=f'**Uploading...**',parse_mode='markdown')
            await client.send_audio(
                chat_id=a.chat.id,
                audio=f'videos/{n}.mp3',
                caption=f'**Title:** {vid.title}',
                file_name=vid.title
            )
    except Exception as e:
        await client.send_message(a.chat.id,f'**Exception**\n`{e}`','md')
    rmfile(f'videos/{n}.mp3')
    rmfile(f'videos/{filename}')
    logging.info('VIDEO LOCALLY REMOVED')
    await a.delete()



def sys_info():
    t1,t2,t3 = psutil.getloadavg()
    cc = os.cpu_count()
    cu = psutil.cpu_percent()
    r = psutil.virtual_memory()[2]
    msg = f'''
**Load Avg**: `{t1} {t2} {t3}`
**CPU Usage**: `{cu}%`
**CPUs**: `{cc}`
**RAM Usage**: `{r}%`
    '''
    return msg



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



def genkeyboard(streams,link,typ):
    kb=[]
    streams = list(streams)
    while len(streams) != 0:
        lel=[]
        for x in streams[:3]:
            lel.append(InlineKeyboardButton(
                text=f'{round(x.filesize/10**6,2)}MB' if typ=='audio' else f'{x.resolution}'
                ,callback_data=f'{link}|{x.itag}'))
            streams.remove(x)
        kb.append(lel)
    return InlineKeyboardMarkup(kb)




WELCOME = '''
Hi there, you can use me to download videos and audios from YouTube just by providing its link!

**Use /help for commands**
'''


HELP = '''
**Usage**

/ytvid `VIDEO_LINK` : Downloads videos from YouTube
/ytaud `VIDEO_LINK`` : Downloads videos as mp3
/ping : Shows bot response time
/help : Display this message
'''