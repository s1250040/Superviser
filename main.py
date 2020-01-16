from flask import Flask, request, abort
import os

import datetime
import schedule
import time

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
#push用環境変数追加
line_user_id = os.getenv('LINE_USER_ID', None)

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#pushメッセージ追加
def main():
    messages = TextSendMessage(text="こんにちは")
    line_bot_api.push_message(line_user_id, messages=messages)

# schedule.every().day.at("23:06").do(main)
main()



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # main()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
