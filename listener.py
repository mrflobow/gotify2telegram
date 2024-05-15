import os
import requests
import json
import websocket

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GOTIFY_HOST = os.getenv("GOTIFY_HOST")
GOTIFY_TOKEN = os.getenv("GOTIFY_TOKEN")



def ws_on_message(ws,message):
    msg = json.loads(message)

    message = msg["message"]
    title = msg['title']

    text = f"<b>{title}</b>\n{message}"

    bot_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=HTML&disable_web_page_preview=1"
    r  = requests.get(bot_url)
    if r.status_code == 200:
        print("Message send")

def ws_on_error(ws, error):
    print(error)

def ws_on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def ws_on_open(ws):
    print("Opened connection")


def main():
    wsapp = websocket.WebSocketApp(f"ws://{GOTIFY_HOST}/stream", header={"X-Gotify-Key": str(GOTIFY_TOKEN)},
                              on_open=ws_on_open,
                              on_message=ws_on_message,
                              on_error=ws_on_error,
                              on_close=ws_on_close)
    wsapp.run_forever()

if __name__ == '__main__':
    main()


