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

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/vgFbdDK.jpg',
                    title='參加網聚',
                    text='請問你想參加哪一場網聚',
                    actions=[
                        PostbackAction(
                            label='2021/5/1',
                            display_text='我想參加2021/5/1的時段',
                            data='action=meetup&itemid=1'
                        ),
                        PostbackAction(
                            label='2021/6/1',
                            display_text='我想參加2021/6/1的時段',
                            data='action=meetup&itemid=2'
                        ),
                        PostbackAction(
                            label='2021/7/1',
                            display_text='我想參加2021/7/1的時段',
                            data='action=meetup&itemid=3'
                        )
                        # MessageAction(
                        #     label='message1',
                        #     text='message text1'
                        # ),
                        # URIAction(
                        #     label='uri1',
                        #     uri='http://example.com/1'
                        # )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/SYP9lpm.jpg',
                    title='線上家教',
                    text='請預約線上家教的時段',
                    actions=[
                        PostbackAction(
                            label='2021/5/1',
                            display_text='我想參加2021/5/1的時段',
                            data='action=tutor&itemid=1'
                        ),
                        PostbackAction(
                            label='2021/6/1',
                            display_text='我想參加2021/6/1的時段',
                            data='action=tutor&itemid=2'
                        ),
                        PostbackAction(
                            label='2021/7/1',
                            display_text='我想參加2021/7/1的時段',
                            data='action=tutor&itemid=3'
                        )
                        # MessageAction(
                        #     label='message2',
                        #     text='message text2'
                        # ),
                        # URIAction(
                        #     label='uri2',
                        #     uri='http://example.com/2'
                        # )
                    ]
                )
            ]
        )
    )

    line_bot_api.reply_message(event.reply_token, carousel_template_message)
    

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