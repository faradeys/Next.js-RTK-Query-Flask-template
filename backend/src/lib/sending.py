import requests
import json
import datetime
from xml.etree import ElementTree
from urllib.parse import unquote

from flask import current_app
from flask_mail import Mail, Message
from src.lib.access import generate_mail_change_code
from src.lib.utils import get_config, generate_short_url
from src.db.models import ServiceParams


mail = Mail()

discord_url = 'https://discordapp.com/api/webhooks/'


def send_email(email, subject=None, html=None, attachments=None):
    sender = (current_app.config['SENDER_NAME'],
              current_app.config['SENDER_MAIL'])
    msg = Message(
        sender=sender,
        recipients=[email],
        subject=subject,
        html=html,
        attachments=attachments)
    mail.send(msg)


def send_verify_email_code(email):
    verify_code = generate_mail_change_code(email)
    if verify_code:
        subject = 'Подтверждение email'
        body = "Ваш проверочный код для смены email <h4><b>"+verify_code+"</b></h4>"
        send_email(email, subject, body)


def send_sms(text, phone, log=False):
    if not phone:
        return False
    if phone[0] == '8':
        phone = '7'+phone[1:]
    elif phone[0] == '+':
        phone = phone[1:]
    elif not phone[0] == '7':
        phone = '7'+phone

    if (get_config('DEBUG') and not log) or phone == '71111111111':
        text = 'номер:' + phone + ' msg:' + text
        order_notification(text)
        return True

    # if len(text) >= 70 and not represents_int(text[66]): #fix for redsms api, who loses 67's symbol (if it not int) in case of sms split because of too many symbols
    #     text = text[:66]+text[65:]

    req_payload = {
        'login': current_app.config['SMS_LOGIN'],
        'password': current_app.config['SMS_PASS'],
        'originator': current_app.config['SMS_SENDER_NAME'],
        'phones': phone,
        'want_sms_ids': 1,
        'rus': 5,
        'message': text
    }

    try:
        resp = requests.get(
            'http://api.smstraffic.ru/multi.php', params=req_payload)
    except requests.exceptions.ConnectionError:
        return False

    if resp.content:
        parsed_resp = ElementTree.fromstring(resp.content)
    if not parsed_resp and not parsed_resp.findtext('code') == '0':
        return False
    return resp


def sms_order_notify(phone, passw=None, order_from=None, order_id=None):

    now = datetime.datetime.now()
    hour_moscow = now.hour + 3
    hour_text = ''
    if hour_moscow >= 21 or hour_moscow < 10:
        hour_text = ' после 10.00'
    if order_from == 'framecs' or order_from == 'framesv' or order_from == 'frame-ym' or order_from == 'localhost:8008':
        url_dpr = 'https://' + order_from + '.damprodam.ru/order-details/' + order_id
        short_url = generate_short_url(url_dpr)

        if short_url:
            url_dpr = short_url.replace('https://', '')

        sms_text = 'Заявка в работе, ожидайте звонка' + hour_text + \
            '. Ваш расчет ' + url_dpr + ' Есть вопросы? +74993488478'
    else:
        sms_text = 'Заявка в работе, ждите звонка. Ваш расчет dampr.ru/a +74993488478'
        if passw:
            sms_text += ' Логин: ' + phone + ' пароль: ' + passw
    send_sms(sms_text, phone)


def order_notification(msg):
    telegram_order_chat = current_app.config['TELEGRAM_ORDER_CHAT']
    telegram_order_token = current_app.config['TELEGRAM_ORDER_TOKEN']
    admin_phone = current_app.config['ADMIN_PHONE']
    ret = 0

    if telegram_order_chat and telegram_order_token:
        # requests.post(
        #     'https://damprodam.ru/gapi/notice/telegram/send_msg_order',
        #     headers={'Content-Type': 'application/json'},
        #     data=json.dumps({
        #         "chat_id": telegram_order_chat,
        #         "token": telegram_order_token,
        #         "msg": msg,
        #         "buttons": 1
        #     })
        # )
        tg_reg = requests.post(
            'https://api.telegram.org/bot' + telegram_order_token + '/sendMessage',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "chat_id": telegram_order_chat,
                "text": msg,
                "parse_mode": "HTML",
                "reply_markup": {
                    "inline_keyboard": reply_markup()
                },
                # "buttons": 1
            })
        )
        tg_reg_json = tg_reg.json()
        if not tg_reg_json or not tg_reg_json['ok']:
            send_discord(msg + '\n\n **телега лежит**', True)
            # if admin_phone:
            #     send_sms('телега прилегла', admin_phone, True)
        else:
            ret = tg_reg_json['result']['message_id']

    send_discord(msg)
    return ret

def telegram_msg(order, sell_device_price=None, promo_code_order=None, promo_code=None,  user=None, partner_charge=None, is_admin_msg=None):
    old_model_info = str()
    for k, x in order.order_info['sell_device']['params'].items():
        if x:
            if k == 'model':
                old_model_info += "- " + str(x[0]) + ": " + str(x[1]) + " " + order.order_info['sell_device']['color'] + "\r\n"
            else:
                old_model_info += "- " + str(x[0]) + ": " + str(x[1]) + "\r\n"
    if is_admin_msg:
        type_order = "<b>Информация о заказе</b>\r\n\r\n"
    else:
        type_order = order.order_info['type_order']
        type_order = "<b>Новый заказ на " + type_order + "</b>\r\n\r\n"

    msg =   "{type_order}" \
            "Продаваемое устройство:\r\n" \
            "{model_info}" \
            "- Состояние: {damaged}\r\n" \
            "- Недостатки: {disadvantages}\r\n" \
            "- Цена: {price}\r\n" \
            "Имя клиента: {name}\r\n" \
            "Номер телефона: {phone}\r\n" \
            "Город: {city}\r\n" \
    .format(**dict(
        type_order=type_order,
        model_info=old_model_info,
        damaged=order.order_info['sell_device']['damaged'],
        disadvantages=order.order_info['sell_device']['disadvantages'].replace('#',', '),
        price=sell_device_price,
        name=order.order_info['name'],
        phone=order.order_info['phone'],
        city=order.order_info['city'],
    ))

    if not order.sell_only and order.order_info['new_device']:
        new_model_info = str()
        if order.new_device:
            for k, x in order.order_info['new_device']['params'].items():
                if x:
                    if k == 'model':
                        new_model_info += "- "+ str(x[0]) +": "+ str(x[1]) +" "+ order.order_info['new_device']['color'] +"\r\n"
                    else:
                        new_model_info += "- "+ str(x[0]) +": "+ str(x[1]) +"\r\n"
                        
        msg += "\r\nПриобретаемое устройство:\r\n" \
            "{n_model_info}" \
            "- Цена: {n_price}\r\n" \
            "- Необходимая доплата: {n_excess_fare}\r\n\r\n" \
        .format(**dict(
            n_model_info=new_model_info,
            n_price=order.order_info['new_device']['price'],
            n_excess_fare=order.order_info['new_device']['excess_fare'],
        ))

    if order.order_info['data_transfer']:
        msg += "Перенос данных: к цене +{data_transfer}\r\n" \
        .format(**dict(
            data_transfer=order.order_info['data_transfer']
        ))
    if order.order_info['stick_glass']:
        msg += "Наклейка стекла: к цене +{stick_glass}\r\n" \
        .format(**dict(
            stick_glass=order.order_info['stick_glass']
        ))
    if (order.order_info['stick_glass'] or order.order_info['data_transfer']) and order.order_info['new_device']:
        if not isinstance(order.order_info['new_device']['excess_fare'], str) and int(order.order_info['new_device']['excess_fare']) > 0:
            msg += "Полная стоимость: {final_price}\r\n\r\n" \
            .format(**dict(
                final_price=int(order.order_info['new_device']['excess_fare'])+int(order.order_info['stick_glass'])+int(order.order_info['data_transfer'])
            ))
    if promo_code_order:
        msg += "Промокод: {promo_code}\r\n" \
                "- Номинал промокода: {promo_code_price}\r\n" \
        .format(**dict(
            promo_code=promo_code.code,
            promo_code_price=promo_code.price
        ))
    if order.order_info['comment']:
        msg += "Комментарий: {comment}\r\n" \
        .format(**dict(
            comment=order.order_info['comment']
        ))
    if order.order_info['meet_time']:
        msg += "Удобное время: {meet_time}\r\n" \
        .format(**dict(
            meet_time=order.order_info['meet_time']
        ))
    if order.order_info['when_time']:
        msg += "Удобный день: {when_time}\r\n" \
        .format(**dict(
            when_time=order.order_info['when_time']
        ))
    if order.order_info['add_items']:
        msg += "Добавил технику: {add_items}\r\n" \
        .format(**dict(
            add_items=order.order_info['add_items']
        ))
    if order.order_info['utm']:
        msg += "Utm: {utm}\r\n" \
        .format(**dict(
            utm=unquote(order.order_info['utm'])
        ))
    if order.order_info['order_from']:
        msg += "Заказ из: {order_from}\r\n" \
        .format(**dict(
            order_from=unquote(order.order_info['order_from'])
        ))

    if user and user.bonuses:
        bonuses_for_order = ServiceParams.get_by_uname('bonuses_for_order')
        bonuses_for_order = int(bonuses_for_order.spec_value) if bonuses_for_order else 2000
        msg += "\r\nБонусы:\r\n" \
            "- По данной сделке: {bonuses}\r\n" \
            "- Всего бонусов: {bonuses_all}\r\n" \
        .format(**dict(
            bonuses=bonuses_for_order,
            bonuses_all=user.bonuses
        ))
        # bonuses=1000 if order.sell_only else user.bonuses,

    if order.referal_code:
        msg += "\r\nРеферал код: {referal_code}\r\n" \
        .format(**dict(
            referal_code=order.referal_code
        ))
    if partner_charge:
        msg += "\r\nПартнёрская комиссия(уже есть в цене): {partner_charge}\r\n" \
        .format(**dict(
            partner_charge=partner_charge
        ))
    
    return msg

def internal_error_notification(failed_user):
    send_discord(
        ":scream: **FLASK API INTERNAL SERVER ERROR** :scream: \n\n __Failed user__: " + failed_user, True)


def send_discord(msg, log=False):
    log_token = current_app.config['DISCORD_LOG_TOKEN'] if log else current_app.config['DISCORD_ORDER_TOKEN']
    if log_token:
        requests.post(
            discord_url + log_token,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "content": msg.replace("\r", "").replace("<b>", "**").replace("</b>", "**"),
                "username": "pythonBOT"
            })
        )


def reply_markup():
    return [
        [
            # {"text": "👍", "callback_data": "order_good"},
            {"text": "🚘", "callback_data": "order_master"},
            {"text": "👎", "callback_data": "order_false"},
            {"text": "nedozvon", "callback_data": "order_nocall"},
        ],
        [
            {"text": "photo", "callback_data": "order_photo"},
            {"text": "comment", "callback_data": "order_edit"},
            {"text": "👍", "callback_data": "order_approved"},
        ],
        [
            {"text": "Инструкция iPhone", "callback_data": "instruction_iphone"},
            {"text": "Инструкция MacBook", "callback_data": "instruction_mac"},
        ]
    ]
