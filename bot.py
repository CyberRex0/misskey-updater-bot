from misskey import Misskey
import websockets
import asyncio
import json
import datetime
import sys
import traceback

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
                

asyncio.get_event_loop().run_until_complete(main())