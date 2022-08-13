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
    
app = LineBotApp(channel_secret, channel_access_token)

def callback(request):
    try:
        app.serve(request)
    except:
        traceback.print_exc()
        return 'ERROR'
    return 'OK'