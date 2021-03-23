# import flask related
from flask import Flask, request, abort
from urllib.parse import parse_qsl
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    VideoSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage
)
import json

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi('oOwChDe8tZ3O/b50XlIQYERmIpiTvmJ2qrA8BwVLrN9K3kiPmhLz+Kgxgo+GT3DTX9F6U05Kg2Nc5WYmb07Cv/35JMlAdGyipUcViY51hCG0triNF3K71Zw135UVn9dg1B1ti6q5ZNy/HEoJkqcE3wdB04t89/1O/w1cDnyilFU=')
# your linebot message API - Channel secret
handler = WebhookHandler('a16278e5ab83fd4d9f72808bd4fed198')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# handle msg
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info & message
    user_id = event.source.user_id
    msg = event.message.text
    user_name = line_bot_api.get_profile(user_id).display_name
    
    # get msg details
    print('msg from [', user_name, '](', user_id, ') : ', msg)

    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/w1JM4f5.jpg',
            title='問一下唷~',
            text='請問你想喝哪一種飲料',
            actions=[
                PostbackAction(
                    label='晚點喝',
                    display_text='我想晚點再喝',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='我想喝茶',
                    text='給我一杯茶吧'
                ),
                MessageAction(
                    label='我想喝咖啡',
                    text='比較想喝咖啡'
                ),
                URIAction(
                    label='想查一下營養資訊',
                    uri='tel:+886933333252'
                )
            ]
        )
    )


    line_bot_api.reply_message(event.reply_token, buttons_template_message)


@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)
    print(parse_qsl(event.postback.data))
    print(dict(parse_qsl(event.postback.data)))
    data=dict(parse_qsl(event.postback.data))
    print(data['action'])

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)