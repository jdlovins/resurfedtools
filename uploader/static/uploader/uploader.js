/**
 * Created by Josh on 11/13/17.
 */
$(document).ready(function () {

    var $uploader_form = $('#uploader-form');
    var $map_author = $('#id_map_author');
    var $map_type = $('#id_map_type');
    var $map_tier = $('#id_map_tier');
    var $map_zones = $('#id_map_zones');
    var $map_bonuses = $('#id_map_bonuses');
    var $map_pre_hop = $('#id_map_disable_pre_hop');
    var $map_baked_triggers = $('#id_map_enable_baked_triggers');
    var $map_spawns = $('#id_map_spawns');
    var $map_repalce = $('#id_replace_map');
    var $map_delete = $('#id_delete_map');
    var $map_list = $('#id_map_list');
    var $file_drop = $('#drag-label');

    $uploader_form.formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
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
            map_author: {
                validators: {
                    notEmpty: {
                        message: 'The username is required'
                    }
                }
            }
        }
    });

    var fv = $uploader_form.data('formValidation');

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

    $map_delete.change(function () {
        if ($(this).prop('checked')) {
            $map_list.prop('disabled', false);
        }
        else {
            if (!$map_repalce.prop('checked')) {
                $map_list.prop('disabled', true);
            }
        }
    });

    $map_repalce.change(function () {
        if ($(this).prop('checked')) {
            $map_list.prop('disabled', false);
        }
        else {
            if (!$map_delete.prop('checked')) {
                $map_list.prop('disabled', true);
            }
        }
    });


    $(document).on('change', ':file', function () {
        var input = $(this),
            numFiles = input.get(0).files ? input.get(0).files.length : 1,
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        console.log(input.get(0).files);
        input.trigger('fileselect', [numFiles, label]);
    });

    // We can watch for our custom `fileselect` event like this
    $(':file').on('fileselect', function (event, numFiles, label) {

        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

        if (input.length) {
            input.val(log);
        } else {
            if (log) alert(log);
        }

    });





    $file_drop.on('dragenter', function (e) {
        e.preventDefault();
        e.stopPropagation();
    });

    $file_drop.on('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('hover');
    });

    $file_drop.on('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('hover');
    });

    $file_drop.on('drop', function (e) {
        e.preventDefault();
        var file = e.originalEvent.dataTransfer.files[0];
        $file_drop.val(file.name);
        $(this).removeClass('hover');
    });

    //$filedrag.css('display', 'block');

});
