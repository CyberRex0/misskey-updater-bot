from misskey import Misskey
import websockets
import asyncio, aiohttp
import json
import datetime
import sys
import traceback
import re
import math

import config

WS_URL = f'wss://{config.MISSKEY_INSTANCE}/streaming?i={config.MISSKEY_TOKEN}'
msk = Misskey(config.MISSKEY_INSTANCE, i=config.MISSKEY_TOKEN)
i = msk.i()

MY_ID = i['id']
print('Bot user id: ' + MY_ID)

async def on_post_note(note):
    if note.get('mentions'):
        print(note['mentions'])
        if MY_ID in note['mentions']:
            print('Command Detected')
            content = note['text'].split(' ', 1)[1].strip()

            if content == 'ping':

                postdate = datetime.datetime.fromisoformat(note['createdAt'][:-1]).timestamp()
                nowdate = datetime.datetime.utcnow().timestamp()
                sa = nowdate - postdate
                text = f'{sa*1000:.2f}ms'
                msk.notes_create(text=text, reply_id=note['id'])

            update_cmd = re.findall(r'v(.*)にアップデートして', content)
            if update_cmd:
                version = update_cmd[0]

                if not (note['user']['id'] in config.ALLOWED_USERS):
                    msk.notes_create(text='許可されたユーザーのみが実行できます', reply_id=note['id'])
                    return

                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.github.com/repos/misskey-dev/misskey/tags') as r:
                        tags = await r.json()
                        for tag in tags:
                            if tag['name'] == version:
                                msk.notes_create(text='アップデートやっとく', reply_id=note['id'])

                                args = [config.UPDATE_SCRIPT_PATH, version]

                                try:
                                    update_proc = await asyncio.create_subprocess_exec('/bin/bash', *args, cwd=config.MISSKEY_DIR)
                                except:
                                    msk.notes_create(text='アップデートできなかった', reply_id=note['id'])
                                    return
                                st = datetime.datetime.utcnow().timestamp()
                                code = await update_proc.wait()
                                if code != 0:
                                    msk.notes_create(text=f'アップデートできなかった({code})', reply_id=note['id'])
                                    return
                                else:
                                    nt = datetime.datetime.utcnow().timestamp()
                                    t = nt - st
                                    tm = math.floor(t / 60)
                                    ts = math.floor(t % 60)
                                    msk.notes_create(text=f'アップデートできたよ (実行時間: {t/60:02.0f}分{t%60:02.0f}秒)\n30秒後に再起動する', reply_id=note['id'])
                                    await asyncio.sleep(30)
                                    # 任意で再起動スクリプト実行
                                    args = [config.RESTART_SCRIPT_PATH]
                                    await asyncio.create_subprocess_exec('/bin/bash', *args)
                                    return
                                
                        else:
                            msk.notes_create(text=f'{version}←そんなの　ない', reply_id=note['id'])

async def on_followed(user):
    try:
        msk.following_create(user['id'])
    except:
        pass

async def main():

    print('Connecting to ' + config.MISSKEY_INSTANCE + '...', end='')
    async with websockets.connect(WS_URL) as ws:
        print('OK')
        print('Attemping to watching timeline...', end='')
        p = {
            'type': 'connect',
            'body': {
                'channel': 'homeTimeline',
                'id': 'HTL1'
            }
        }
        await ws.send(json.dumps(p))
        print('OK')
        p = {
            'type': 'connect',
            'body': {
                'channel': 'main'
            }
        }
        await ws.send(json.dumps(p))
        
        print('Listening ws')
        while True:
            data = await ws.recv()
            j = json.loads(data)
            print(j)

            if j['type'] == 'channel':
                if j['body']['type'] == 'note':
                    note = j['body']['body']
                    try:
                        await on_post_note(note)
                    except Exception as e:
                        print(traceback.format_exc())
                        continue
                if j['body']['type'] == 'followed':
                    try:
                        await on_followed(j['body']['body'])
                    except Exception as e:
                        print(traceback.format_exc())
                        continue
                

reconnect_counter = 0

while True:
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        break
    except:
        reconnect_counter += 1
        print('Reconnecting...', end='')
        if reconnect_counter > 10:
            print('Too many reconnects. Exiting.')
            sys.exit(1)
        continue