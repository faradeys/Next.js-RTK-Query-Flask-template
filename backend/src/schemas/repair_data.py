from webargs import fields, validate

macbook_buyout_params_post = {
    'models_macbooks': fields.Str(),
    'memory': fields.Str(),
    'ram': fields.Str(),
    'inches': fields.Str(),
    'touch_bar': fields.Str(),
    'year': fields.Integer(),
    'is_retina': fields.Bool(),
    'cpu': fields.Str(required=False),
}

macbook_tradein_params_post = {
    'models_macbooks': fields.Str(),
    'memory': fields.Str(),
    'cpu': fields.Str(),
    'gpu': fields.Str(),
    'ram': fields.Str(),
    'inches': fields.Str(),
    'year': fields.Integer(),
    'touch_bar': fields.Str()
}

macbook_buyout_price_post = {
    'models_macbooks': fields.Str(required=True),
    'memory': fields.Str(required=True),
    'ram': fields.Str(required=True),
    'inches': fields.Str(required=True),
    'touch_bar': fields.Str(required=True),
    'year': fields.Integer(required=True),
    'is_retina': fields.Bool(required=True),
    'damaged': fields.Bool(missing=True),
    'scratches': fields.Str(),
    'chips': fields.Str(),
    'keyboard': fields.Str(),
    'legs': fields.Str(),
    'battery_life': fields.Str(),
    'dents': fields.Str(),
    'gap': fields.Str(),
    'anti_reflect': fields.Str(),
    'cpu': fields.Str(),
    'order_from': fields.Str(),
}

macbook_tradein_price_post = {
    'models_macbooks': fields.Str(required=True),
    'memory': fields.Str(required=True),
    'cpu': fields.Str(required=True),
    'ram': fields.Str(required=True),
    'inches': fields.Str(required=True),
    'year': fields.Integer(required=True),
    'touch_bar': fields.Str(required=True),
    'gpu': fields.Str()
}

macbook_tradein_order_post = {
    'old_mac': fields.Nested({
        'id': fields.UUID(required=True),
        'damaged': fields.Bool(required=True),
        'scratches': fields.Str(),
        'chips': fields.Str(),
        'keyboard': fields.Str(),
        'legs': fields.Str(),
        'battery_life': fields.Str(),
        'dents': fields.Str(),
        'gap': fields.Str(),
        'anti_reflect': fields.Str(),
    }, required=True),
    'new_mac': fields.Nested({
        'id': fields.UUID(required=True),
        'color': fields.Str(required=True)
    }),
    'sell_only': fields.Bool(required=True),
    'name': fields.Str(required=True),
    'phone': fields.Str(required=True),
    'city': fields.Str(required=True),
    'comment': fields.Str(),
    'meet_time': fields.Str(),
    'when_time': fields.Str(),
    'add_items': fields.Str(),
    'utm': fields.Str(),
    'referrer_code': fields.Str()
}

accessories_buyout_params_post = {
    'accessories_device': fields.Str(),
    'model': fields.Str(),
    'memory': fields.Str(),
    'keyboard_conf': fields.Str()
}

accessories_buyout_price_post = {
    'accessories_device': fields.Str(required=True),
    'model': fields.Str(),
    'memory': fields.Str(),
    'keyboard_conf': fields.Str(),
    'accessory_equipment': fields.Str(),
    'keyboard_of_mouse_keyboard': fields.Str(),
    'disk_count': fields.Integer(),
    'gamepad_count': fields.Integer(),
    'damaged': fields.Bool(required=True),
    'is_repaired': fields.Bool(required=True),
    'order_from': fields.Str(),
    'exterier_condition': fields.Str(),
}

dyson_buyout_params_post = {
    'model': fields.Str()
}

dyson_buyout_price_post = {
    'dyson_equipment': fields.Str(),
    'acc': fields.Str(),
    'dyson_device': fields.Str(),
    'model': fields.Str(),
    'exterier_condition': fields.Str(),
    'kit': fields.Str(),
}

robocleaner_buyout_params_post = {
    'model': fields.Str()
}

robocleaner_buyout_price_post = {
    'model': fields.Str(),
    'robocleaner_acc': fields.Str(),
    'robocleaner_device': fields.Str(),
    'robocleaner_condition': fields.Str(),
    'equipment_robocleaner': fields.Str(),
    'panel_replacement': fields.Str(),
}

iphone_buyout_params_post = {
    'models_iphones': fields.Str(),
    'memory': fields.Str(),
    'order_from': fields.Str()
}

iphone_buyout_price_post = {
    'models_iphones': fields.Str(required=True),
    'memory': fields.Str(required=True),
    'equipment_iphone': fields.Str(required=True),
    'restored_display': fields.Str(required=True),
    'exterier_condition': fields.Str(required=True),
    'battery_condition': fields.Str(),
    'order_from': fields.Str(),
    'damaged': fields.Bool(required=True)
}

iphone_tradein_price_post = {
    'models_iphones': fields.Str(required=True),
    'memory': fields.Str(required=True)
}

iphone_tradein_params_post = {
    'models_iphones': fields.Str(),
    'memory': fields.Str()
}

iphone_tradein_order_post = {
    'old_iphone': fields.Nested({
        'id': fields.UUID(required=True),
        'damaged': fields.Bool(required=True),
        'equipment_iphone': fields.Str(required=True),
        'restored_display': fields.Str(required=True),
        'exterier_condition': fields.Str(required=True)
    }, required=True),
    'new_iphone': fields.Nested({
        'id': fields.UUID(required=True),
        'color': fields.Str(required=True)
    }),
    'sell_only': fields.Bool(required=True),
    'name': fields.Str(required=True),
    'phone': fields.Str(required=True),
    'city': fields.Str(required=True),
    'comment': fields.Str(),
    'when_time': fields.Str(),
    'utm': fields.Str(),
    'referrer_code': fields.Str()
}

ipad_buyout_params_post = {
    'models_ipads': fields.Str(),
    'cellular': fields.Str(),
    'memory': fields.Str()
}

ipad_buyout_price_post = {
    'models_ipads': fields.Str(required=True),
    'memory': fields.Str(required=True),
    'cellular': fields.Str(required=True),
    'equipment_ipad': fields.Str(required=True),
    'exterier_condition_ipad': fields.Str(required=True),
    'order_from': fields.Str(),
}

ipad_tradein_params_post = {
    'models_ipads': fields.Str(),
    'cellular': fields.Str(),
    'memory': fields.Str()
}

ipad_tradein_price_post = {
    'models_ipads': fields.Str(required=True),
    'cellular': fields.Str(required=True),
    'memory': fields.Str(required=True)
}

android_buyout_params_post = {
    'vendor': fields.Str(),
    'models_android': fields.Str(),
    'memory': fields.Str(),
    'order_from': fields.Str(),
}

android_buyout_price_post = {
    'vendor': fields.Str(required=True),
    'models_android': fields.Str(required=True),
    'memory': fields.Str(required=True),
    # 'equipment_android': fields.Str(required=True),
    # 'restored_display': fields.Str(required=True),
    'exterier_condition_android': fields.Str(required=True),
    # 'damaged': fields.Bool(required=True)
    'order_from': fields.Str(),
}

notebook_buyout_price_post = {
    'vendor': fields.Str(required=True),
    'models_notebook': fields.Str(required=True),
    'exterier_condition_notebook': fields.Str(required=True),
}

samsung_buyout_params_post = {
    'models_samsung': fields.Str(),
    'memory': fields.Str()
}

samsung_buyout_price_post = {
    'models_samsung': fields.Str(required=True),
    'memory': fields.Str(required=True),
    'equipment_samsung': fields.Str(required=True),
    'restored_display': fields.Str(required=True),
    'exterier_condition_samsung': fields.Str(required=True),
    'damaged': fields.Bool(required=True)
}

samsung_tradein_params_post = {
    'models_samsung': fields.Str(),
    'memory': fields.Str()
}

samsung_tradein_price_post = {
    'models_samsung': fields.Str(required=True),
    'memory': fields.Str(required=True)
}

samsung_tradein_order_post = {
    'old_samsung': fields.Nested({
        'id': fields.UUID(required=True),
        'damaged': fields.Bool(required=True),
        'equipment_samsung': fields.Str(required=True),
        'restored_display': fields.Str(required=True),
        'exterier_condition_samsung': fields.Str(required=True)
    }, required=True),
    'new_samsung': fields.Nested({
        'id': fields.UUID(required=True),
        'color': fields.Str(required=True)
    }),
    'sell_only': fields.Bool(required=True),
    'name': fields.Str(required=True),
    'phone': fields.Str(required=True),
    'city': fields.Str(required=True),
    'comment': fields.Str(),
    'when_time': fields.Str(),
    'utm': fields.Str(),
    'referrer_code': fields.Str()
}

cross_tradein_order_post = {
    'old_device': fields.Nested({
        'id': fields.UUID(required=True),
        'device_sell_type': fields.Str(required=True),
        'damaged': fields.Bool(),
        'color': fields.Str(),
        'battery_condition': fields.Str(),
        #iphone and samsung
        'restored_display': fields.Str(),
        # accessories
        'accessory_equipment': fields.Str(),
        'accessories_device': fields.Str(),
        'is_repaired': fields.Bool(),
        'keyboard_of_mouse_keyboard': fields.Str(),
        'disk_count': fields.Integer(),
        'gamepad_count': fields.Integer(),
        # iphone
        'equipment_iphone': fields.Str(),
        'exterier_condition': fields.Str(),
        # ipad
        'equipment_ipad': fields.Str(),
        'exterier_condition_ipad': fields.Str(),
        # samsung
        'equipment_samsung': fields.Str(),
        'exterier_condition_samsung': fields.Str(),
        # android
        'exterier_condition_android': fields.Str(),
        # macbook
        'scratches': fields.Str(),
        'chips': fields.Str(),
        'keyboard': fields.Str(),
        'legs': fields.Str(),
        'battery_life': fields.Str(),
        'dents': fields.Str(),
        'gap': fields.Str(),
        'anti_reflect': fields.Str(),
        # apple watches
        'equipment_watches': fields.Str(),
        'exterier_condition_watches': fields.Str(),
        # notebook
        'equipment_notebook': fields.Str(),
        'exterier_condition_notebook': fields.Str(),
        # dyson
        'dyson_equipment': fields.Str(),
        'acc': fields.Str(),
        'model': fields.Str(),
        'dyson_device': fields.Str(),
        'exterier_condition': fields.Str(),
        'kit': fields.Str(),
        'extra_device': fields.Str(),
        # robocleaner
        'equipment_robocleaner': fields.Str(),
        'robocleaner_acc': fields.Str(),
        'robocleaner_device': fields.Str(),
        'robocleaner_condition': fields.Str(),
        'panel_replacement': fields.Str(),
    }, required=True),
    'new_device': fields.Nested({
        'id': fields.UUID(required=True),
        'color': fields.Str(required=True),
        'device_sell_type': fields.Str(required=True),
    }),
    'sell_only': fields.Bool(required=True),
    'name': fields.Str(required=True),
    'phone': fields.Str(required=True),
    'city': fields.Str(required=True),
    'comment': fields.Str(),
    'meet_time': fields.Str(),
    'when_time': fields.Str(),
    'add_items': fields.Str(),
    'stick_glass': fields.Str(),
    'data_transfer': fields.Str(),
    'utm': fields.Str(),
    'save_calc_data': fields.Str(),
    'save_calc_type': fields.Str(),
    'save_calc_id': fields.Str(),
    'referrer_code': fields.Str(),
    'order_from': fields.Str(),
    'promo_code': fields.Str(),
    'telegram_id': fields.Str(),
    'telegram_username': fields.Str(),
    'lang': fields.Str()
}

watches_buyout_params_post = {
    'models_watches': fields.Str(),
    'size_mm': fields.Str()
}

watches_buyout_price_post = {
    'models_watches': fields.Str(required=True),
    'size_mm': fields.Str(required=True),
    'equipment_watches': fields.Str(required=True),
    'exterier_condition_watches': fields.Str(required=True),
    'order_from': fields.Str(),
}

watches_tradein_params_post = {
    'models_watches': fields.Str(),
    'size_mm': fields.Str()
}

watches_tradein_price_post = {
    'models_watches': fields.Str(required=True),
    'size_mm': fields.Str(required=True)
}

telegram_update_post = {
    'callback_query': fields.Nested({
        'message': fields.Nested({
            'message_id': fields.Integer(),
            'chat': fields.Nested({
                'id': fields.Str()
            }),
            'date': fields.Str(),
            'text': fields.Str(),
        }),
        'from': fields.Nested({
            'username': fields.Str(),
            'id': fields.Integer(),
        }),
        'data': fields.Str(),
        'device_sell_type': fields.Str(),
    }),
    'message': fields.Nested({
        'from': fields.Nested({
            'username': fields.Str(),
            'id': fields.Str(),
        }),
        'text': fields.Str(),
    }),
}

repair_order_post = {
    'name': fields.Str(),
    'phone': fields.Str(required=True),
    'model': fields.Str(required=True),
    'damages': fields.List(fields.Str()),
    'problems': fields.List(fields.Str()),
    'serviceType': fields.Str(required=True),
    'typeConnection': fields.Str()
}
