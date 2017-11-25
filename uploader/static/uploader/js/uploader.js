/**
 * Created by Josh on 11/13/17.
 */
$(window).bind("load", function () {


    $('.ui.fluid').dropdown();

    var $uploader_form = $('#uploader-form');
    var $map_author = $('#id_map_author');
    var $map_type = $('#id_map_type');
    var $map_tier = $('#id_map_tier');
    var $map_zones = $('#id_map_zones');
    var $map_bonuses = $('#id_map_bonuses');
    var $map_pre_hop = $('#id_map_disable_pre_hop');
    var $map_baked_triggers = $('#id_map_enable_baked_triggers');
    var $map_spawns = $('#id_map_spawns');
    var $map_replace = $('#id_replace_map');
    var $map_delete = $('#id_delete_map');
    var $map_list = $('#id_map_list');
    var $file_label = $('#file_label');
    var $submit_button = $('#submit-form-btn');
    var $progress = $('#progress-bar');
    var $log = $('#logs');
    var fv = $uploader_form.data('formValidation');

    var file = null;
    var connected = false;
    var reply_channel = null;

    var actions = {
        reply_channel: "reply_channel",
        form_error: "form_error",
        general_error: "general_error",
        started_task: "started_task",
        progress_update: "progress_update",
        message: "message"
    };

    var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/socket";
    var socket = new ReconnectingWebSocket(ws_path);


    $map_list.parent().addClass("disabled");

    $uploader_form.formValidation({
        framework: 'bootstrap',
        excluded: ':disabled',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            map_author: {
                validators: {
                    notEmpty: {
                        message: 'The map author is required'
                    },
                    stringLength: {
                        max: 32,
                        min: 1,
                        message: 'The map author needs to be at least 1 letter and less than 32.'
                    }
                }
            },
            map_type: {
                validators: {
                    notEmpty: {
                        message: 'You should never see this!'
                    }
                }
            },
            servers: {
                validators: {
                    notEmpty: {
                        message: "Please select at least one server."
                    }
                }
            },
            map_spawns: {
                validators: {
                    callback: {
                        message: 'Invalid format!',
                        callback: function (value, validator, $field) {

                            var text = $map_spawns.val();

                            if (text.length === 0)
                                return true;

                            var pattern = /^(map::-?\d+,-?\d+,-?\d+:-?\d+,-?\d+,-?\d+|(stage|bonus):([1-9]\d*):-?\d+,-?\d+,-?\d+:-?\d+,-?\d+,-?\d+)$/;

                            var lines = text.split("\n");

                            var ret_value = true;

                            $.each(lines, function (i) {
                                if (!pattern.test(lines[i])) {
                                    ret_value = false;
                                    return false;
                                }
                            });
                            return ret_value;
                        }
                    }
                }
            },
            map_list: {
                validators: {
                    notEmpty: {
                        message: "You need to choose a map to replace / delete"
                    }
                }
            },
            file_input: {
                validators: {
                    notEmpty: {
                        message: "You ned to upload a map."
                    }
                }
            }
        }
    });


    function log_message(message) {
        $log.append('<p>' + message + '</p><br/>')
    }


    // handles enabling or disabling all the Map Information stuff
    $('#id_insert_map_info').change(function () {
        if ($(this).prop('checked')) {

            $map_author.removeAttr("disabled");
            $map_type.removeAttr("disabled");
            $map_zones.removeAttr("disabled");
            $map_tier.removeAttr("disabled");
            $map_bonuses.removeAttr("disabled");
            $map_pre_hop.removeAttr("disabled");
            $map_baked_triggers.removeAttr("disabled");
            $map_spawns.removeAttr("disabled");


        } else {

            fv.resetField($map_author);
            fv.resetField($map_type);
            fv.resetField($map_zones);
            fv.resetField($map_tier);
            fv.resetField($map_bonuses);
            fv.resetField($map_pre_hop);
            fv.resetField($map_baked_triggers);
            fv.resetField($map_spawns);

            $map_author.prop('disabled', true);
            $map_type.prop('disabled', true);
            $map_zones.prop('disabled', true);
            $map_tier.prop('disabled', true);
            $map_bonuses.prop('disabled', true);
            $map_pre_hop.prop({'disabled': true, 'checked': false});
            $map_baked_triggers.prop({'disabled': true, 'checked': false});
            $map_spawns.prop('disabled', true);

        }
    });

    $map_replace.change(function () {
        var l_fv = $uploader_form.data('formValidation');
        if ($(this).prop('checked')) {
            $map_list.parent().removeClass("disabled");
            $map_list.prop("disabled", false);
        }
        else {
            if (!$map_delete.prop('checked')) {
                $map_list.parent().addClass("disabled").dropdown('clear');
                l_fv.resetField($map_list);
                $map_list.prop("disabled", true);
            }
        }
    });

    $map_delete.change(function () {
        var l_fv = $uploader_form.data('formValidation');
        if ($(this).prop('checked')) {
            $map_list.parent().removeClass("disabled");
            $map_list.prop("disabled", false);
        }
        else {
            if (!$map_replace.prop('checked')) {
                $map_list.parent().addClass("disabled").dropdown('clear');
                l_fv.resetField($map_list);
                $map_list.prop("disabled", true);
            }
        }
    });


    $(document).on('change', ':file', function (e) {
        var input = $(this),
            numFiles = input.get(0).files ? input.get(0).files.length : 1,
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        file = input.get(0).files[0];
        $submit_button.prop('disabled', false);
        input.trigger('fileselect', [numFiles, label]);
    });

    // We can watch for our custom `fileselect` event like this
    $(':file').on('fileselect', function (event, numFiles, label) {

        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

        if (input.length) {
            input.val(log);
        }

    });


    $file_label.on('dragenter', function (e) {
        e.preventDefault();
        e.stopPropagation();
    });

    $file_label.on('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('hover');
    });

    $file_label.on('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('hover');
    });

    $file_label.on('drop', function (e) {

        e.preventDefault();
        $(this).removeClass('hover');

        var t_file = e.originalEvent.dataTransfer.files[0];

        if (!t_file.name.match(/.bsp$/)) {

            BootstrapDialog.show({
                title: "What are you doing?",
                message: '<h1>You can only upload .bsp files!</h1><br/><br/>' +
                '<img src="https://i.imgur.com/MWUKggh.gif" />',
                type: BootstrapDialog.TYPE_DANGER,
                buttons: [{
                    hotkey: 13,
                    label: 'Ok, Sorry :(',
                    cssClass: 'btn-primary',
                    action: function (dialogItself) {
                        dialogItself.close();
                    }
                }]
            });
            return;
        }

        file = t_file;
        $file_label.val(file.name);

        var l_fv = $uploader_form.data('formValidation');
        l_fv.updateStatus('file_input', "VALID");

    });

    socket.onopen = function () {
        log_message('Connected to uploader backend...');
        connected = true;
    };

    socket.onclose = function () {
        connected = false;
    };

    socket.onmessage = function (message) {
        console.log("Got message: " + message.data);
        var packet = JSON.parse(message.data);

        switch(packet.action) {
            case actions.reply_channel:
                reply_channel = packet.data;
                break;

            case actions.progress_update:
                var percent = packet.data;
                $progress.css('width', percent + '%').attr('aria-valuenow', percent).text(percent + "%");
                console.log(percent);
                if (percent === 100)
                    $progress.removeClass('progress-bar-info').addClass('progress-bar-success');
                break;

            case actions.message:
                log_message(packet.data);
                break;
        }
    };

    function collectFormData() {
        // Go through all the form fields and collect their names/values.
        var fd = new FormData(this);


        $("form#uploader-form :input").each(function () {
            var $this = $(this);
            var name = $this.attr("name");
            var type = $this.attr("type") || "";
            var value = $this.val();

            if (name === undefined) {
                return;
            }

            if (type === "file") {
                return;
            }

            if (type === "checkbox" || type === "radio") {
                if (!$this.prop("checked")) {
                    return;
                }
                value = true;
            }

            console.log(name + " - " + value);

            fd.append(name, value);
        });

        fd.append("file", file);
        fd.append("reply_channel", reply_channel);

        return fd;
    }

    $submit_button.click(function (e) {

        e.preventDefault();

        var l_fv = $uploader_form.data('formValidation');

        l_fv.validateField($("#id_servers"));
        l_fv.validateField($("#id_map_list"));
        l_fv.validateField($("#id_file_input"));
        if (!l_fv.isValid()) {
            return;
        }

        $submit_button.prop('disabled', true);

        var fd = collectFormData();

        $.ajax({
            xhr: function () {
                var xhrobj = $.ajaxSettings.xhr();
                if (xhrobj.upload) {
                    xhrobj.upload.addEventListener("progress", function (event) {
                        var percent = 0;
                        var position = event.loaded || event.position;
                        var total = event.total;

                        if (event.lengthComputable) {
                            percent = Math.ceil(position / total * 100);
                        }

                        console.log(percent);
                        $progress.css('width', percent + '%').attr('aria-valuenow', percent).text(percent + "%");

                        if (percent === 100) {
                            $progress.removeClass('progress-bar-info').addClass('progress-bar-success');
                        }

                    }, false)
                }
                return xhrobj;
            },
            url: '/uploader',
            method: "POST",
            contentType: false,
            processData: false,
            cache: false,
            data: fd,
            dataType: 'json',
            success: function (response) {
                switch (response.action) {

                    case actions.form_error:
                        console.log(response.data['errors']);

                        var error_list = response.data['errors'];

                        var error_message = '';

                        for (var key in error_list) {
                            if (error_list.hasOwnProperty(key)) {
                                for (var error in error_list[key]) {
                                    if (error_list[key].hasOwnProperty(error)) {
                                        error_message += "<p>" + key + '  -  ' + error_list[key][error] + "</p><br/>";
                                    }
                                }
                            }
                        }

                        BootstrapDialog.show({
                            title: "Something went wrong!",
                            message: error_message,
                            type: BootstrapDialog.TYPE_DANGER,
                            buttons: [{
                                hotkey: 13,
                                label: 'Close',
                                cssClass: 'btn-primary',
                                action: function (dialogItself) {
                                    dialogItself.close();
                                }
                            }]
                        });

                        $progress.removeClass('progress-bar-success').addClass('progress-bar-danger');

                        break;


                    case actions.general_error:

                        BootstrapDialog.show({
                            title: "Something went wrong!",
                            message: response.data,
                            type: BootstrapDialog.TYPE_DANGER,
                            buttons: [{
                                hotkey: 13,
                                label: 'Close',
                                cssClass: 'btn-primary',
                                action: function (dialogItself) {
                                    dialogItself.close();
                                }
                            }]
                        });

                        $progress.removeClass('progress-bar-success').addClass('progress-bar-danger');
                        break;

                    case actions.started_task:
                        $progress.removeClass('progress-bar-success').addClass('progress-bar-info');
                        break;
                }
                //$submit_button.prop("disabled", false);
            }
        });
    });
});
