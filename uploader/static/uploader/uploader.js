/**
 * Created by Josh on 11/13/17.
 */
$(document).ready(function () {
    $("#input-id").fileinput({
        uploadUrl: '/file-upload-batch/2',
        maxFilePreviewSize: 10240,
        showUpload: true,
        //showPreview: false,
        showUploadedThumbs: false,
        mainClass: "input-group-lg",
        fileActionSettings: {
            showUpload: false
        },
        preferIconicPreview: true, // this will force thumbnails to display icons for following file extensions
        previewFileIconSettings: { // configure your icon file extensions
            'bsp': '<i class="fa fa-map text-primary"></i>',
        },
        previewFileExtSettings: { // configure the logic for determining icon file extensions
            'bsp': function (ext) {
                return ext.match(/(bsp)$/i);
            }
        }
    });


});