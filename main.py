import os
import sys
import traceback

from app import LineBotApp

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# 一個實例只有一個 app
app = LineBotApp(channel_secret, channel_access_token)

def callback(request):
    try:
        # 事件來時呼叫 app 處理
        app.serve(request)
    except:
        # 發生錯誤寫入記錄檔
        traceback.print_exc()
        return 'ERROR'
    return 'OK'