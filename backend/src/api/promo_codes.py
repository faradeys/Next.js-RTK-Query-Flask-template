import time
from datetime import datetime
import pytz

from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import session, db
from src.db.models import PromoCodes, ServiceParams
from src.schemas.promo_codes import check_promo_code_post


class CheckPromoCodeAPI(Resource):
    @use_args(check_promo_code_post)
    def post(self, data):
        promo_code = data.get('promo_code')
        
        device_type = data.get('device_type')
        order_type = data.get('order_type')
        price = data.get('price')
        fcode_device_type = None
        code = None
        codes = PromoCodes.find(promo_code)
        if codes:
            for fcode in codes:
                if fcode.type:
                    fcode_device_type = ServiceParams.query.filter_by(id=fcode.type).first()
                    if fcode_device_type:
                        if fcode_device_type.u_name == 'model':
                            fcode_device_type = ServiceParams.query.filter_by(id=fcode_device_type.parent_id).first()
                        if fcode_device_type.u_name == device_type:
                            if fcode.order_type:
                                if fcode.order_type == order_type:
                                    code = fcode
                            else:
                                code = fcode
                else:
                    code = fcode

        if not code:
            return {
                "message": "Промокод не существует"
            }, 404


        if code.order_type and code.order_type != order_type:
            return {"message": "Промокод не подходит под данный тип заявки"}, 403

        # if code.type:
        #     fcode_device_type = ServiceParams.query.filter_by(id=fcode.type).first()
        #     if fcode_device_type:
        #         if fcode_device_type.u_name == 'model':
        #             fcode_device_type = ServiceParams.query.filter_by(id=fcode_device_type.parent_id).first()
        #         if code.type != fcode_device_type.id:
        #             return {"message": "Промокод не подходит под данный тип устройства"}, 403

        if (code.min_price and code.min_price > price) or (code.max_price and code.max_price < price):
            return {"message": "Промокод не подходит под данную цену"}, 403

        if code.started_at or code.ends_at:
            tz_msc = pytz.timezone("Europe/Moscow")
            time_now = datetime.now(tz_msc)
            if code.started_at:
                started_at = tz_msc.localize(code.started_at.replace(tzinfo=None))
                if time_now < started_at:
                    return {"message": "Срок действия промокода еще не наступил"}, 403
            if code.ends_at:
                ends_at = tz_msc.localize(code.ends_at.replace(tzinfo=None))
                if time_now > ends_at:
                    return {"message": "Срок действия промокода закончился"}, 403
        
        if code.price:
            return {
                "price": code.price
            }