from flask import Flask, request, abort
import os

import datetime
import schedule
import time
import random
import re
import sqlite3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageAction, ButtonsTemplate
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

# #pushメッセージ追加
# def main():
#     messages = make_button_template()
#     line_bot_api.push_message(line_user_id, messages=messages)

# # schedule.every().day.at("04:35").do(main)
# main()

# while True:
#   schedule.run_pending()
#   time.sleep(60)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == str(ANSWER):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='正解です')
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='不正解です')
        )

#idを元に問題を選択
def get_question(number):
    dbname = 'question.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select_sql = "select question from questioninfo where id =='"+str(number)+"'"
    c.execute(select_sql)
    result = c.fetchone()
    conn.close()
    return result[0]


def get_choice1(number):
    dbname = 'question.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select_sql = "select one from questioninfo where id =='"+str(number)+"'"
    c.execute(select_sql)
    result = c.fetchone()
    conn.close()
    return result


def get_choice2(number):
    dbname = 'question.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select_sql = "select two from questioninfo where id =='"+str(number)+"'"
    c.execute(select_sql)
    result = c.fetchone()
    conn.close()
    return result

def get_choice3(number):
    dbname = 'question.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select_sql = "select three from questioninfo where id =='"+str(number)+"'"
    c.execute(select_sql)
    result = c.fetchone()
    conn.close()
    return result

def get_choice4(number):
    dbname = 'question.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select_sql = "select four from questioninfo where id =='"+str(number)+"'"
    c.execute(select_sql)
    result = c.fetchone()
    conn.close()
    return result

def get_answer(number):
    dbname = 'question.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select_sql = "select answer from questioninfo where id =='"+str(number)+"'"
    c.execute(select_sql)
    result = c.fetchone()
    conn.close()
    return result


def make_button_template():
    global ANSWER
    number = random.randint(1,3)
    question = get_question(number)
    choice1 = get_choice1(number)
    choice2 = get_choice2(number)
    choice3 = get_choice3(number)
    choice4 = get_choice4(number)
    ANSWER = get_answer(number)
    message_template = TemplateSendMessage(
        alt_text="問題",
        template=ButtonsTemplate(
            text=question,
            actions=[
                MessageAction(
                    label=choice1,
                    text="1"
                ),
                MessageAction(
                    label=choice2,
                    text="2"
                ),
                MessageAction(
                    label=choice3,
                    text="3"
                ),
                MessageAction(
                    label=choice4,
                    text="4"
                ),
            ]
        )
    )
    return message_template

#pushメッセージ追加
def main():
    button_message = TextSendMessage(make_button_template())
    line_bot_api.push_message(line_user_id, messages=button_message)

# schedule.every().day.at("04:35").do(main)
main()

while True:
  schedule.run_pending()
  time.sleep(60)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
