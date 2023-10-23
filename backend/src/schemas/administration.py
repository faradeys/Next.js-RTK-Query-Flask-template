from webargs import fields, validate


login_post = {
    'email': fields.Str(required=True, validate=validate.Length(min=1)),
    'password': fields.Str(required=True, validate=validate.Length(min=1))
}

service_params_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'parent': fields.Str(),
        'name': fields.Str(required=True, validate=validate.Length(min=1)),
        'u_name': fields.Str(required=True, validate=validate.Length(min=1)),
        'spec_value': fields.Str(),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'parent': fields.Str(),
        'name': fields.Str(required=True, validate=validate.Length(min=1)),
        'u_name': fields.Str(required=True, validate=validate.Length(min=1)),
        'spec_value': fields.Str(),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

disadvantages_iphone_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'parent': fields.Str(),
        'u_name': fields.Str(required=True, validate=validate.Length(min=1)),
        'spec_value': fields.Str(),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'parent': fields.Str(),
        'u_name': fields.Str(required=True, validate=validate.Length(min=1)),
        'spec_value': fields.Str(),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

watches_tradein_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_watches': fields.Str(required=True, validate=validate.Length(min=1)),
        'size_mm': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_watches': fields.Str(required=True, validate=validate.Length(min=1)),
        'size_mm': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

watches_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_watches': fields.Str(required=True, validate=validate.Length(min=1)),
        'size_mm': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price_best': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_watches': fields.Str(required=True, validate=validate.Length(min=1)),
        'size_mm': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price_best': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True)
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

phone_repair_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'phone_repair': fields.Str(required=True, validate=validate.Length(min=1)),
        'service_id': fields.UUID(required=True),
        'price1': fields.Integer(required=True),
        'price2': fields.Str(),
        'sale': fields.Str(),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'phone_repair': fields.Str(required=True, validate=validate.Length(min=1)),
        'price1': fields.Integer(required=True),
        'price2': fields.Str(),
        'sale': fields.Str(),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

glass_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'service_id': fields.UUID(required=True),
        'price1': fields.Integer(required=True),
        # 'price2': fields.Str(),
        'device': fields.Str(required=True, validate=validate.Length(min=1)),
        'service_name': fields.Str(),
    }, required=True)),    
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'service_id': fields.UUID(required=True),
        'price1': fields.Integer(required=True),
        # 'price2': fields.Str(),
        'device': fields.Str(required=True, validate=validate.Length(min=1)),
        'service_name': fields.Str(),
    }, required=True)),   
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)), 
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

huawei_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_huawei': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_huawei': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True)
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

companies_charge_update_post = {
    'new_entries': fields.List(fields.Nested({
        'company_id': fields.Str(required=True, validate=validate.Length(min=1)),
        'price_from': fields.Integer(required=True),
        'price_to': fields.Integer(required=True),
        'charge': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'company_id': fields.Str(required=True, validate=validate.Length(min=1)),
        'price_from': fields.Integer(required=True),
        'price_to': fields.Integer(required=True),
        'charge': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

android_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'vendor': fields.Str(required=True, validate=validate.Length(min=1)),
        'models_android': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        # 'min_price': fields.Integer(required=True),
        # 'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True),
        'margin': fields.Integer(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'vendor': fields.Str(required=True, validate=validate.Length(min=1)),
        'offer_id': fields.UUID(required=True),
        'models_android': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        # 'min_price': fields.Integer(required=True),
        # 'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True),
        'margin': fields.Integer(required=True)
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}


device_colors_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'color': fields.Str(required=True, validate=validate.Length(min=1)),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'device_type': fields.Str(required=True, validate=validate.Length(min=1)),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'color': fields.Str(required=True, validate=validate.Length(min=1)),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'device_type': fields.Str(required=True, validate=validate.Length(min=1)),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

companies_excluded_models_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'company': fields.UUID(required=True),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'device_type': fields.Str(required=True, validate=validate.Length(min=1)),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'company': fields.UUID(required=True),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'device_type': fields.Str(required=True, validate=validate.Length(min=1)),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

notebook_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'vendor': fields.Str(required=True, validate=validate.Length(min=1)),
        'models_notebook': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        # 'min_price': fields.Integer(required=True),
        # 'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        # 'price_normal': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'vendor': fields.Str(required=True, validate=validate.Length(min=1)),
        'offer_id': fields.UUID(required=True),
        'models_notebook': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        # 'min_price': fields.Integer(required=True),
        # 'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        # 'price_normal': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}


samsung_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_samsung': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_samsung': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True)
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

samsung_tradein_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_samsung': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_samsung': fields.Str(required=True),
        'memory': fields.Str(required=True),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}


ipad_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_ipads': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'cellular': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_bad': fields.Integer(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_ipads': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'cellular': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_bad': fields.Integer(required=True)
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}


ipad_tradein_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_ipads': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'cellular': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_ipads': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'cellular': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

iphone_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_iphones': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True),
        'price_market': fields.Integer()
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_iphones': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_normal': fields.Integer(required=True),
        'price_market': fields.Integer()
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

iphone_tradein_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_iphones': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'price': fields.Integer(required=True),
        'vendor_code': fields.Str(default=''),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_iphones': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'price': fields.Integer(required=True),
        'vendor_code': fields.Str(default=''),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

accessories_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'accessories_device': fields.Str(required=True, validate=validate.Length(min=1)),
        'model': fields.Str(required=True),
        'memory': fields.Str(),
        'keyboard_conf': fields.Str(),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
        'price_repaired': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'accessories_device': fields.Str(required=True, validate=validate.Length(min=1)),
        'model': fields.Str(required=True),
        'memory': fields.Str(),
        'keyboard_conf': fields.Str(),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
        'price_repaired': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

macbook_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_macbooks': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'ram': fields.Str(required=True, validate=validate.Length(min=1)),
        'inches': fields.Str(required=True, validate=validate.Length(min=1)),
        'touch_bar': fields.Str(required=True, validate=validate.Length(min=1)),
        'year': fields.Integer(required=True),
        'vendor_code': fields.Str(default=''),
        'is_retina': fields.Bool(required=True),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price': fields.Integer(required=True),
        'tradein_price': fields.Integer(required=True),
        'cpu': fields.Str()
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_macbooks': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'ram': fields.Str(required=True, validate=validate.Length(min=1)),
        'inches': fields.Str(required=True, validate=validate.Length(min=1)),
        'touch_bar': fields.Str(required=True, validate=validate.Length(min=1)),
        'year': fields.Integer(required=True),
        'vendor_code': fields.Str(default=''),
        'is_retina': fields.Bool(required=True),
        'min_price': fields.Integer(required=True),
        'max_price': fields.Integer(required=True),
        'price': fields.Integer(required=True),
        'tradein_price': fields.Integer(required=True),
        'cpu': fields.Str()
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

macbook_tradein_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'models_macbooks': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'cpu': fields.Str(required=True, validate=validate.Length(min=1)),
        'ram': fields.Str(required=True, validate=validate.Length(min=1)),
        'inches': fields.Str(required=True, validate=validate.Length(min=1)),
        'touch_bar': fields.Str(required=True, validate=validate.Length(min=1)),
        'year': fields.Integer(required=True),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
        'apple_price': fields.Integer(required=True),
        'gpu': fields.Str(required=True)
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'models_macbooks': fields.Str(required=True, validate=validate.Length(min=1)),
        'memory': fields.Str(required=True, validate=validate.Length(min=1)),
        'cpu': fields.Str(required=True, validate=validate.Length(min=1)),
        'ram': fields.Str(required=True, validate=validate.Length(min=1)),
        'inches': fields.Str(required=True, validate=validate.Length(min=1)),
        'touch_bar': fields.Str(required=True, validate=validate.Length(min=1)),
        'year': fields.Integer(required=True),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
        'apple_price': fields.Integer(required=True),
        'gpu': fields.Str(required=True)
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

dyson_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'device': fields.Str(required=True, validate=validate.Length(min=1)),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_bad': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'device': fields.Str(required=True, validate=validate.Length(min=1)),
        'offer_id': fields.UUID(required=True),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price_best': fields.Integer(required=True),
        'price_well': fields.Integer(required=True),
        'price_bad': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

robocleaner_buyout_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'device': fields.Str(required=True, validate=validate.Length(min=1)),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'device': fields.Str(required=True, validate=validate.Length(min=1)),
        'offer_id': fields.UUID(required=True),
        'model': fields.Str(required=True, validate=validate.Length(min=1)),
        'vendor_code': fields.Str(default=''),
        'price': fields.Integer(required=True),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}

user_info_post = {
    'search_str': fields.Str(),
    'search_id_str': fields.Str()
}

referal_info_post ={
    'search_str': fields.Str(required=True)
}

fboffload_post = {
    'begins': fields.Str(),
    'ends': fields.Str()
}

priceload_post = {
    'type': fields.Str(),
}

priceupload_post = {
    'uptype': fields.Str(),
}

ordersload_post = {
    'begins': fields.Str(),
    'ends': fields.Str(),
    'type': fields.Str(),
}

user_updates_post = {
    'changed_entries': fields.List(fields.Nested({
        'user_id': fields.UUID(required=True),
        'phone': fields.Str(required=True, missing=None),
        'name': fields.Str(required=True, missing=None),
        'city': fields.Str(required=True, missing=None),
        'email': fields.Str(required=True, missing=None),
        'bonuses': fields.Integer(required=True, missing=0)
    }, required=True))
}

password_update = {
    'new_pass': fields.Str(required=True),
    'user_phone': fields.Str(required=True),
}

promo_codes_updates_post = {
    'promocode_date': fields.Str(),
    'new_entries': fields.List(fields.Nested({
        'code': fields.Str(required=True),
        'started_at': fields.Str(),
        'ends_at': fields.Str(),
        'price': fields.Integer(required=True),
        'min_price': fields.Str(),
        'max_price': fields.Str(),
        'order_type': fields.Str(),
        'device_type': fields.Str(),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'code_id': fields.UUID(required=True),
        'code': fields.Str(required=True),
        'started_at': fields.Str(),
        'ends_at': fields.Str(),
        'price': fields.Integer(required=True),
        'min_price': fields.Str(),
        'max_price': fields.Str(),
        'order_type': fields.Str(),
        'device_type': fields.Str(),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'code_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'code_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'code_id': fields.UUID(required=True)
    }, required=True))
}

revmap_post = {
    'codes': fields.Str(required=True),
    'sms-text': fields.Str(required=True),
    'bonuses': fields.Integer(required=True)
}

iphone_repair_updates_post = {
    'new_entries': fields.List(fields.Nested({
        'broken_part': fields.Str(),
        'models_iphones': fields.Str(),
        'price': fields.Str(required=True),
        'problem': fields.Str(),
    }, required=True)),
    'changed_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True),
        'broken_part': fields.Str(),
        'models_iphones': fields.Str(),
        'price': fields.Str(required=True),
        'problem': fields.Str(),
    }, required=True)),
    'deprecated_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'respawn_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True)),
    'purge_entries': fields.List(fields.Nested({
        'offer_id': fields.UUID(required=True)
    }, required=True))
}