import json

from django.http import HttpResponse
from django.shortcuts import render
from home.decorators import custom_login_required, custom_permission_required
from django.contrib import messages
import uploader.strings as strings
from .choices import MapType, MapTypeChoices

from .forms import UploadForm


# Create your views here.


@custom_login_required
@custom_permission_required('home.access_uploader', messages.WARNING, strings.NO_UPLOADER_ACCESS)
def uploader(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():

            if 'file' not in request.FILES:
                print("missing file")

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

                print(map_spawns)

            if request.user.has_perm('home.uploader_advanced'):
                replace_map = form.cleaned_data.get('replace_map')
                delete_map = form.cleaned_data.get('delete_map')
                map_choice = int(0 if form.cleaned_data.get('map_list') is '' else form.cleaned_data.get('map_list'))
                print(map_choice)
                if (replace_map or delete_map) and map_choice == 0:
                    print("we error")
                    # kick back an error
                    pass
                map_choice = form.fields['map_list'].choices[map_choice]
                # form.fields['map_list'].choices




        else:
            print(form.errors)

        resp = json.dumps({"data": "blah!"})
        return HttpResponse(resp, content_type='application/json')

    form = UploadForm()
    return render(request, 'uploader.html', {'form': form})
