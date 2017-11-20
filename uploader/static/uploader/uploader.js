/**
 * Created by Josh on 11/13/17.
 */
$(document).ready(function () {

    // handles enabling or disabling all the Map Information stuff
    $('#' + form_ids['map_information']).change(function () {
        if ($(this).prop('checked')) {
            $('#' + form_ids['map_author']).removeAttr("disabled");
            $('#' + form_ids['map_type']).removeAttr("disabled");
            $('#' + form_ids['map_zones']).removeAttr("disabled");
            $('#' + form_ids['map_tier']).removeAttr("disabled");
            $('#' + form_ids['map_bonuses']).removeAttr("disabled");
            $('#' + form_ids['map_prehop']).removeAttr("disabled");
            $('#' + form_ids['map_baked']).removeAttr("disabled");
        } else {
            $('#' + form_ids['map_author']).prop('disabled', true);
            $('#' + form_ids['map_type']).prop('disabled', true);
            $('#' + form_ids['map_zones']).prop('disabled', true);
            $('#' + form_ids['map_tier']).prop('disabled', true);
            $('#' + form_ids['map_bonuses']).prop('disabled', true);
            $('#' + form_ids['map_prehop']).prop({'disabled': true, 'checked': false});
            $('#' + form_ids['map_baked']).prop({'disabled': true, 'checked': false});
        }
    });

});
