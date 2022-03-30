# variables for the bot (env vars by default)
# if you're deploying locally then set NON_LOCAL to False and 
# fill the values in the `else` block

import os

NON_LOCAL = True

if NON_LOCAL:
    API_ID = int(os.environ.get('API_ID'))
    API_HASH = str(os.environ.get('API_HASH'))
    BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))
    try:LOG_GRP_ID = int(os.environ.get('LOG_GRP_ID'))
    except:LOG_GRP_ID = 0
else:
    API_ID = 123 # get it from my.telegram.org
    API_HASH = '123abc' # get it from my.telegram.org
    BOT_TOKEN = '123:abc' # get it from @BotFather
    LOG_GRP_ID = 123 # [OPTIONAL] create a group and add @MissRose_bot and send /id to get 
    # chat id