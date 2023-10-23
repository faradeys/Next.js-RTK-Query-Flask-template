import imaplib, email, re
from flask import current_app
from src.db.models import User, UserTextStore
from src.lib.sending import order_notification, send_sms
from src.lib.utils import parse_phone
from src.db import session

reg_exp_tel_list = [r'Телефон[ :\t]*(\+7 \(\d{3}\)[ ]\d{3}[ -]\d{2}[ -]\d{2})', r'Телефон[ :]*(\+\d*)']
reg_exp_name = r'Имя[ :\t]*(\w*[ \t]*\w*)'
reg_exp_second_name = r'Фамилия[ :\t]*(\w*[ \t]*\w*)'
reg_exp_yandex = r'яндекс[ ]*'

def use_reg_exp(body, reg_exp_tel_list, reg_exp_name, reg_exp_second_name):
    reg_exp_del_list = [r'<.*>', r'>', r'Адреса магазинов((\n*).*)*']

    for reg_exp_del in reg_exp_del_list:
        body = re.sub(reg_exp_del, '', body)

    name_msg = '- Имя: яндекс '
    telephone_msg = '- Телефон: '

    for reg_exp in reg_exp_tel_list:
        telephone = re.search(reg_exp, body, flags=re.MULTILINE)
        if telephone:
            telephone_msg += telephone.group(1)
            break

    if re.search(reg_exp_name, body, flags=re.MULTILINE):
        name_msg += re.search(reg_exp_name, body, flags=re.MULTILINE).group(1)

    if re.search(reg_exp_second_name, body, flags=re.MULTILINE):
        name_msg += (' ' + re.search(reg_exp_second_name, body, flags=re.MULTILINE).group(1))

    if 'От пользователя Яндекс Маркета' in body:
        middle_part = body.rpartition('Создана заявка')[1]
        end_part = body.rpartition('Создана заявка')[2]
        body = middle_part + end_part

    body = name_msg + '\n' + telephone_msg + '\n\n' + body

    return body

def get_email():
    PARSE_EMAIL_URL = current_app.config['PARSE_EMAIL_URL']

    try:
        imap = imaplib.IMAP4_SSL(current_app.config['IMAP_SERVER_URL'])
        imap.login(current_app.config['PARSE_EMAIL_LOGIN'], current_app.config['PARSE_EMAIL_PASSWORD'])
    except:
        print('failed to connect to mail server')
        return

    if imap:
        imap.select("inbox")
        _, msgnums = imap.uid('search', None, 'UNSEEN')
        body = ''
        count_mails = 0
        sended_msgs = 0
        created_stores = 0

        if len(msgnums[0]) == 0:
            return

        for msgnum in msgnums[0].split():
            _, data = imap.uid('fetch', msgnum, '(RFC822)')
            message = email.message_from_bytes(data[0][1])
            message_from = message.get('From')
            match_mail = False

            for em in PARSE_EMAIL_URL:
                if message_from.find(em) != -1:
                    is_send = False
                    match_mail = True
                    count_mails += 1

                    for part in message.walk():
                        message_id = None
                        user_phone = None
                        user_name = None
                        body = None
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True)
                            body = body.decode()
                            body = use_reg_exp(body, reg_exp_tel_list, reg_exp_name, reg_exp_second_name)

                            message_id = order_notification(body)
                            is_send = True
                            sended_msgs += 1

                        if part.get_content_type() == 'text/html' and is_send == False:
                            body = part.get_payload(decode=True)
                            body = body.decode()
                            reg_exp_tag = r'<.*?>|&nbsp;|&amp;'
                            body = re.sub(reg_exp_tag, '', body)
                            body = use_reg_exp(body, reg_exp_tel_list, reg_exp_name, reg_exp_second_name)

                            message_id = order_notification(body)
                            sended_msgs += 1

                        if body:
                            for reg_exp in reg_exp_tel_list:
                                telephone = re.search(reg_exp, body, flags=re.MULTILINE)
                                if telephone:
                                    user_phone = telephone.group(1)
                                    break

                            user_phone =  parse_phone(user_phone)

                            if re.search(reg_exp_name, body, flags=re.MULTILINE):
                                user_name = re.search(reg_exp_name, body, flags=re.MULTILINE).group(1)
                                user_name = re.sub('яндекс ', '', user_name)

                            if re.search(reg_exp_second_name, body, flags=re.MULTILINE):
                                user_name += (' ' + re.search(reg_exp_second_name, body, flags=re.MULTILINE).group(1))

                            if re.search(reg_exp_yandex, body, flags=re.MULTILINE):
                                body = re.sub(reg_exp_yandex, '', body)

                        if message_id and user_phone:
                            user_text = UserTextStore(
                                text=body,
                                phone=user_phone,
                                message_id=message_id
                            )
                            if user_name:
                                user_text.name = user_name

                            session.add(user_text)
                            session.commit()

                            created_stores += 1

                            user = User.check_phone_number(user_phone)
                            if not user:
                                user = User.new_one(user_phone)
                                
                            send_sms('Заявка в работе. Мы сейчас позвоним уточнить детали и время встречи. Ваш damprodam 💌 +74993488478', user_phone)


            if not match_mail:
                imap.uid('STORE', msgnum, '-FLAGS', '\Seen')

        imap.close()

        count_str = 'parsed mails: {}, sended msgs: {}, created text stores: {}'.format(count_mails, sended_msgs, created_stores)
        print(count_str)
