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
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage, DatetimePickerAction
)
import json, os, datetime

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi('oOwChDe8tZ3O/b50XlIQYERmIpiTvmJ2qrA8BwVLrN9K3kiPmhLz+Kgxgo+GT3DTX9F6U05Kg2Nc5WYmb07Cv/35JMlAdGyipUcViY51hCG0triNF3K71Zw135UVn9dg1B1ti6q5ZNy/HEoJkqcE3wdB04t89/1O/w1cDnyilFU=')
# your linebot message API - Channel secret
handler = WebhookHandler('a16278e5ab83fd4d9f72808bd4fed198')

@app.route("/")
def index():
    return 'welcome'

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

    if msg == '查詢飯店':
        json_path = os.path.join(os.path.split(__file__)[0], 'json-area.txt')
        with open(json_path, 'r', encoding='UTF-8') as f:
            bubblestring = f.read()
        bubbledict = json.loads(bubblestring)
        bubbledictlist = []

        urllist=['https://i.imgur.com/JERvLX3.jpg', 
                'https://i.imgur.com/j5U7aWN.jpg', 
                'https://i.imgur.com/1cvXCcL.jpg', 
                'https://i.imgur.com/gkgvBJA.jpg']
        contentstextlist=['宜花東飯店', 
                        '台北桃竹苗飯店', 
                        '台中雲彰飯店', 
                        '高雄台南嘉義飯店']
        buttoncontentstextlist=['搜尋宜花東飯店', 
                        '搜尋台北桃竹苗飯店', 
                        '搜尋台中雲彰飯店', 
                        '搜尋高雄台南嘉義飯店']
        actionlist=['action=step1&area=1', 
                    'action=step1&area=2', 
                    'action=step1&area=3', 
                    'action=step1&area=4']
        
        i=0
        for _ in urllist:
            bubbledict['body']['contents'][0]['url']=urllist[i]
            bubbledict['body']['contents'][2]['contents'][0]['contents'][0]['contents'][0]['text']=contentstextlist[i]
            bubbledict['body']['action']['data']=actionlist[i]
            bubbledictlist.append(json.loads(json.dumps(bubbledict.copy()))) 
            i+=1

        flexmessagedict={"type":"carousel"}
        flexmessagedict['contents']=bubbledictlist

        flex_message = FlexSendMessage(
            alt_text='hello',
            contents=flexmessagedict
        )
        # print(flexmessagedict)
        line_bot_api.reply_message(event.reply_token, flex_message)
    

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    print(event.postback.data)
    print(parse_qsl(event.postback.data))
    print(dict(parse_qsl(event.postback.data)))
    data=dict(parse_qsl(event.postback.data))
    # print(data['action'])
    # print(data['area'])
    action = data['action'] if 'action' in data else ''
    area = data['area'] if 'area' in data else ''
    hotel = data['hotel'] if 'hotel' in data else ''
    if (action=='step1' and area=='1'):
        json_path = os.path.join(os.path.split(__file__)[0], 'json-area.txt')
        with open(json_path, 'r', encoding='UTF-8') as f:
            bubblestring = f.read()
        bubbledict = json.loads(bubblestring)
        bubbledictlist = []

        urllist=['https://i.imgur.com/QKpgCUg.jpg', 
                'https://i.imgur.com/bPfgbmA.png']
        contentstextlist=['童樂天親子夢幻民宿', 
                        '涵暄精品民宿']
        actionlist=['action=step2&hotel=1', 
                    'action=step2&hotel=2']
        
        i=0
        for _ in urllist:
            bubbledict['body']['contents'][0]['url']=urllist[i]
            bubbledict['body']['contents'][2]['contents'][0]['contents'][0]['contents'][0]['text']=contentstextlist[i]
            bubbledict['body']['action']['data']=actionlist[i]
            bubbledictlist.append(json.loads(json.dumps(bubbledict.copy()))) 
            i+=1

        flexmessagedict={"type":"carousel"}
        flexmessagedict['contents']=bubbledictlist

        flex_message = FlexSendMessage(
            alt_text='hello',
            contents=flexmessagedict
        )
        # print(flexmessagedict)
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif (action=='step2' and hotel=='1'):
        data = dict(parse_qsl(event.postback.data))
        now = datetime.datetime.now()
        min_now = now + datetime.timedelta(days=3)
        max_now = now + datetime.timedelta(days=180)

        image_carousel_template_message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/L3mU9My.jpg',
                        action=DatetimePickerAction(
                                label="預約飯店入住日期",
                                data=f"action=step3",
                                mode="datetime",
                                initial=f'{min_now:%Y-%m-%dT00:00}',
                                min=f'{min_now:%Y-%m-%dT00:00}',
                                max=f'{max_now:%Y-%m-%dT23:59}'
                            )
                        )
                    # ,
                    # ImageCarouselColumn(
                    #     image_url='https://example.com/item2.jpg',
                    #     action=PostbackAction(
                    #         label='postback2',
                    #         display_text='postback text2',
                    #         data='action=buy&itemid=2'
                    #     )
                    # )
                ]
            )
        )

        line_bot_api.reply_message(
            reply_token = event.reply_token,
            messages = [image_carousel_template_message]
        )
    elif (action=='step3'):
        appointment_datetime = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')
        print(appointment_datetime)
        appointment_tutor_done_text = f'謝謝{user_name}，以幫您預約飯店完成'
        appointment_tutor_done_datetime_text = f'你預約的日期為{appointment_datetime:%Y-%m-%d}，時間是{appointment_datetime:%H:%M}'

        json_path = os.path.join(os.path.split(__file__)[0], 'json-ticket.txt')
        with open(json_path, 'r', encoding='UTF-8') as f:
            bubblestring = f.read()
        bubbledict = json.loads(bubblestring)
        flex_message = FlexSendMessage(alt_text='hello',
                                        contents=bubbledict
                                        )
        # print(flexmessagedict)
        # line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=appointment_tutor_done_text),
        #                                             TextSendMessage(text=appointment_tutor_done_datetime_text),
        #                                             flex_message])
        line_bot_api.reply_message(event.reply_token, flex_message)    


# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)