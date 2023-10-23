$(document).ready(function () {
    $('.action_desc a').click(function (e) {
        e.preventDefault();
        $(this).remove();
        $('.action_desc .action_desc_content').css('display', 'block');
    });

    $('.find_user_btn').click(function () {
        $("#find_user_form").submit();
    });
    
    $('.find_user_id_btn').click(function () {
        $("#find_user_id_form").submit();
    });

    $('.fboffload_form').click(function (e) {
        e.preventDefault();
        $("#fboffload_form").submit();
    });

    $('.uploadgd_prices_form').click(function (e) {
        e.preventDefault();
        $("#upload_prices_form").submit();
    });

    $('#fboffload_form .begins').datetimepicker({
        viewMode: 'months',
        format: 'YYYY-MM-DD'
    });

    $('#fboffload_form .ends').datetimepicker({
        viewMode: 'months',
        format: 'YYYY-MM-DD'
    });

    $('.ordersload_form').click(function (e) {
        e.preventDefault();
        $("#ordersload_form").submit();
    });

    $('#ordersload_form .begins').datetimepicker({
        viewMode: 'months',
        format: 'YYYY-MM-DD'
    });

    $('#ordersload_form .ends').datetimepicker({
        viewMode: 'months',
        format: 'YYYY-MM-DD'
    });
    $('input[name="started_at"],input[name="ends_at"],input[name="promocode_date"]').datetimepicker({
        viewMode: 'months',
        format: 'YYYY-MM-DD H:m',
    }).on("dp.change", function (e) {
        if ($(this)[0]['name'] !== 'promocode_date') {
            var tr = $(e.currentTarget).parent().parent().parent();
            if (!tr.hasClass('new_one')) {
                tr.addClass('changed');
            }
            page_changed();
        }
    });

    $('.order-send-telegram').on('click', function() {
        var orderID = $(this).data('order-info');
        $.ajax({
            url: "/admin/cross_tradein_orders_telegram",
            type: "post",
            data: orderID,
            dataType: "text",
            contentType: "text",
            success: function () {
                if ($('.telegram_send_status_err').is(":visible")) {
                    $('.telegram_send_status_err').hide();
                }
                $('.telegram_send_status_succ').fadeIn(500);
            },
            error: function () {
                if ($('.telegram_send_status_succ').is(":visible")) {
                    $('.telegram_send_status_succ').hide();
                }
                $('.telegram_send_status_err').fadeIn(500);
            }
        });
    });

    if ($('.priceupload-succes').length) {
        setTimeout(function () {
            $('.priceupload-succes').fadeOut(500);
        }, 5000);
    }

    if ($('table.offers_table').length) {
        var page_changed_check = false;
        window.onbeforeunload = function (e) {
            if (page_changed_check) {
                return 'Изменения не сохранены!';
            }
        };

        var new_one = $('table.table tbody tr').eq(1).clone();
        if (!new_one.length) new_one = $('table.table tbody tr').eq(0).clone();
        new_one.find('input, select').val('');
        new_one.addClass('new_one');
        new_one.removeClass('purge');
        new_one.removeClass('changed');
        new_one.removeClass('deprecated_old');
        new_one.find('.deprecated').remove();
        new_one.find('.respawn').remove();

        $('.set-looking-parent').select2({
            placeholder: "Выбрать параметры для родителей",
            width: '700px',
            allowClear: true
        });
        $('.set-looking-parent').on('select2:select', function (e) {
            var this_val = $(this).val();
            if (this_val.length) {
                window.open("/admin/service_params/" + this_val, "_self");
            }
        });
        $('.set-looking-parent').on('select2:unselecting', function (e) {
            window.open("/admin/service_params", "_self");
        });

        $('.select-subject-ser-par-parent').select2({
            placeholder: "Родитель",
            width: '500px',
            allowClear: true
        });

        var updates_offers_type = $('table.table input[name=updates_offers_type]').val();
        if (!updates_offers_type.length) {
            $('.updates_status').fadeOut(500, function () {
                $('.updates_status').css('display', 'none');
                $('.updates_status.alert-danger').text('Отсутствует updates_offers_type ID! Не удастся обновить данные таблицы!');
                $('table.table').css('pointer-events', 'none');
                $('table.table').css('opacity', '0.3');
                $('.updates_status.alert-danger').fadeIn(500);
            });
            return false;
        }

        $('.create_entry').click(function (e) {
            page_changed();
            e.preventDefault();
            var new_entry = $(new_one).clone();
            new_entry.find('.select-subject-ser-par-parent').select2({
                placeholder: "Родитель",
                width: '500px',
                allowClear: true
            });
            $(this).parentsUntil(".card").find('table.table').prepend(new_entry);
        });

        $('table.table').on('click', '.deprecated', function (e) {
            page_changed();
            e.preventDefault();
            var tr = $(this).parent().parent();
            if (tr.hasClass('deprecated')) {
                tr.removeClass('deprecated')
            } else {
                tr.removeClass('purge');
                tr.removeClass('changed');
                tr.addClass('deprecated')
            }
        });

        $('table.table').on('click', '.respawn', function (e) {
            page_changed();
            e.preventDefault();
            var tr = $(this).parent().parent();
            if (tr.hasClass('deprecated_old')) {
                tr.removeClass('deprecated_old');
                tr.removeClass('purge');
                tr.addClass('respawn');
            } else {
                tr.removeClass('respawn');
                tr.addClass('deprecated_old');
            }
        });

        $('table.table').on('click', '.purge', function (e) {
            page_changed();
            e.preventDefault();
            var tr = $(this).parent().parent();
            if (tr.hasClass('purge')) {
                tr.removeClass('purge')
            } else {
                tr.removeClass('deprecated');
                tr.removeClass('changed');
                tr.addClass('purge')
            }
        });

        $('table.table').on('change', 'input, select', function () {
            page_changed();
            var tr = $(this).parent().parent().parent();
            if (!tr.hasClass('new_one')) {
                tr.addClass('changed');
            }
        });

        if (localStorage.getItem('succ_updated') === '1') {
            localStorage.setItem('succ_updated', '0');
            $('.updates_status.alert-success').css('display', 'block');
            setTimeout(function () {
                $('.updates_status.alert-success').fadeOut(500);
            }, 5000);
        }

        $('html').on('click', '.save_all, .promocode_date_btn', function (e) {
            e.preventDefault();
            var data = {};

            var new_promocode_date = $('input[name=promocode_date]');
            if (new_promocode_date.length) {
                data.promocode_date = new_promocode_date.val();
            }

            var new_entries = $('table.table').find('tr.new_one');
            if (new_entries.length) {
                $.extend(true, data, { new_entries: [] });
                $.each(new_entries, function (i, new_entry) {
                    if (!$(new_entry).hasClass('purge')) {
                        var new_entry_data = {};
                        $.each($(new_entry).find('select, input'), function (i2, val) {
                            var val = $(val);
                            if (val.val()) {
                                new_entry_data[val.attr('name')] = val.val();
                            }
                        });
                        if($('.phone_repair').length) {
                            new_entry_data.service_id = $('input[name=service_id]').eq($('input[name=service_id]').length - 1).val()
                        }
                        if($('.glass').length) {
                            new_entry_data.service_id = $('input[name=service_id]').eq($('input[name=service_id]').length - 1).val()
                            new_entry_data.service_name = $('input[name=service_name]').eq($('input[name=service_name]').length - 1).val()
                        }
                        data.new_entries.push(new_entry_data);
                    }
                });
            }

            var changed_entries = $('table.table').find('tr.changed');
            if (changed_entries.length) {
                $.extend(true, data, { changed_entries: [] });
                $.each(changed_entries, function (i, changed_entry) {
                    if (!$(changed_entry).hasClass('purge')) {
                        var changed_entry_data = {};
                        $.each($(changed_entry).find('select, input'), function (i2, val) {
                            var val = $(val);
                            if(val.val()) {
                                changed_entry_data[val.attr('name')] = val.val()
                            }
                        });
                        data.changed_entries.push(changed_entry_data);
                    }
                });
            }

            var deprecated_entries = $('table.table').find('tr.deprecated');
            if (deprecated_entries.length) {
                $.extend(true, data, { deprecated_entries: [] });
                $.each(deprecated_entries, function (i, val) {
                    data.deprecated_entries.push({
                        offer_id: $(val).find('input[name=offer_id]').val(),
                        code_id: $(val).find('input[name=code_id]').val()
                    });
                });
            }

            var respawn_entries = $('table.table').find('tr.respawn');
            if (respawn_entries.length) {
                $.extend(true, data, { respawn_entries: [] });
                $.each(respawn_entries, function (i, val) {
                    data.respawn_entries.push({
                        offer_id: $(val).find('input[name=offer_id]').val(),
                        code_id: $(val).find('input[name=code_id]').val()
                    });
                });
            }

            var purge_entries = $('table.table').find('tr.purge');
            if (purge_entries.length) {
                $.extend(true, data, { purge_entries: [] });
                $.each(purge_entries, function (i, val) {
                    if (!$(val).hasClass('new_one')) {
                        data.purge_entries.push({
                            offer_id: $(val).find('input[name=offer_id]').val(),
                            code_id: $(val).find('input[name=code_id]').val()
                        });
                    }
                });
            }

            $.ajax({
                url: "/admin/" + updates_offers_type + "/updates",
                type: "post",
                data: JSON.stringify(data),
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                timeOut: 15000,
                success: function () {
                    localStorage.setItem('succ_updated', '1');
                    page_changed_check = false;
                    location.reload();
                },
                error: function (data) {
                    if (data.status == 403 || data.status == 422) {
                        $('.updates_status').css('display', 'none');
                        $('.updates_status.alert-warning').text(data.responseJSON.text);
                        $('.updates_status.alert-warning').fadeIn(500);
                    }
                    if (data.status == 404) {
                        $('.updates_status').css('display', 'none');
                        $('.updates_status.alert-danger').text(data.responseJSON.text);
                        $('.updates_status.alert-danger').fadeIn(500);
                    }
                }
            });
        });

        function page_changed() {
            if (!page_changed_check) {
                $('#main-wrapper .navbar-collapse .navbar-nav.my-lg-0').prepend('<a class="save_all pull-right btn btn-warning" href="#">Сохранить</a>');
            }
            page_changed_check = true;
        }

        $('.show_old_deprecated').click(function (e) {
            e.preventDefault();
            $('table.table').addClass('show_deprecated_old');
            $(this).remove();
        })

        $('.models_navigate span').click(function (e) {
            e.preventDefault();
            var goto = $(this).attr('goto');
            $([document.documentElement, document.body]).animate({
                scrollTop: $("#" + goto).offset().top - 70
            }, 300);
        })
    }

    if ($('#change_pass_form').length) {
        var newPass = $('input[name="cp1"]').val()
        var newPassRepeat = $('input[name="cp2"]').val()

        $('.change-pass-input').on('input', function() {
            $('.password_set_status').fadeOut(100);
            if ($(this).attr("name") === 'cp1') {
                newPass = $(this).val()
            }
            if ($(this).attr("name") === 'cp2') {
                newPassRepeat = $(this).val()
            }
        });

        $('.change-password-btn').on('click', function(evt) {
            if (newPass !== newPassRepeat && newPass !== '' && newPassRepeat !== '') {
                evt.preventDefault();
                $('.password_not_exec').fadeIn(100);
            }
            if (newPass === newPassRepeat && newPass !== '' && newPassRepeat !== '') {
                evt.preventDefault();
                var userPhone = $('input[name="phone"]').val();
                var data = {
                    new_pass: newPass,
                    user_phone: userPhone
                };

                $.ajax({
                    url: "/admin/users/new_pass",
                    type: "post",
                    data: JSON.stringify(data),
                    dataType: "json",
                    contentType: "application/json; charset=utf-8",
                    success: function() {
                        $('.password_change_succ').fadeIn(100);
                        $('.change-pass-input').val('');
                    },
                    error: function() {
                        $('.password_smth_wrong').fadeIn(100);
                    }
                });
            }
        });
    }


});
