import json

from django.http import HttpResponse
from django.shortcuts import render
from home.decorators import custom_login_required, custom_permission_required
from django.contrib import messages
import uploader.strings as strings
from .choices import MapType, MapTypeChoices, ActionType
from .helpers import handle_uploaded_file
from resurfedtools.helpers import generate_json_response
from .forms import UploadForm
from .tasks import upload_file
from time import sleep


# Create your views here.


@custom_login_required
@custom_permission_required('uploader.uploader_access', messages.WARNING, strings.NO_UPLOADER_ACCESS)
def uploader(request):
    form = UploadForm(request.user)
    resp = None

    if request.method == 'POST':

        form = UploadForm(request.user, request.POST)

        file_path, reply_channel, map_author, map_type, map_tier, map_zones, map_bonuses, map_disable_pre_hop,\
            map_enable_baked_triggers, map_spawns, replace_map, delete_map, map_choice = [None] * 13

        if form.is_valid():

            reply_channel = request.POST.get('reply_channel')

            if 'file' not in request.FILES:
                resp = generate_json_response(ActionType.GENERAL_ERROR, "missing file")
                return HttpResponse(resp, content_type='application/json')
            else:
                try:
                    file_path = handle_uploaded_file(request.FILES['file'])
                except FileNotFoundError as er:
                    resp = generate_json_response(ActionType.GENERAL_ERROR, "Could not save the file!")
                    return HttpResponse(resp, content_type='application/json')

            insert_map_data = form.cleaned_data.get('insert_map_info')

            if insert_map_data:
                map_author = form.cleaned_data.get('map_author')
                map_type = MapTypeChoices[int(form.cleaned_data.get('map_type'))][1]
                map_tier = form.cleaned_data.get('map_tier')
                map_zones = form.cleaned_data.get('map_zones')
                map_bonuses = form.cleaned_data.get('map_bonuses')
                map_disable_pre_hop = form.cleaned_data.get('map_disable_pre_hop')
                map_enable_baked_triggers = form.cleaned_data.get('map_enable_baked_triggers')
                map_spawns = form.cleaned_data.get('map_spawns')

            if request.user.has_perm('uploader.uploader_admin'):

                replace_map = form.cleaned_data.get('replace_map')
                delete_map = form.cleaned_data.get('delete_map')
                map_choice = int(0 if form.cleaned_data.get('map_list') is '' else form.cleaned_data.get('map_list'))

                if (replace_map or delete_map) and map_choice == 0:
                    resp = generate_json_response(ActionType.GENERAL_ERROR, "Invalid map choice")
                    return HttpResponse(resp, content_type='application/json')

                map_choice = form.fields['map_list'].choices[map_choice]

            servers = [server.id for server in form.cleaned_data.get('servers')]

            upload_task = upload_file.delay(reply_channel, file_path, servers, delete_map, replace_map, map_choice)

            resp = generate_json_response(ActionType.STARTED_TASK, "")

        else:
            errors = {"errors": {}}
            for origin in form.errors:
                sub_error = {origin: []}
                for error in form[origin].errors:
                    sub_error[origin].append(error)
                errors['errors'].update(sub_error)

            resp = generate_json_response(ActionType.FORM_ERROR, errors)

        return HttpResponse(resp, content_type='application/json')

    return render(request, 'uploader.html', {'form': form})
