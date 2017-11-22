from django.shortcuts import render
from home.decorators import custom_login_required, custom_permission_required
from django.contrib import messages
import uploader.strings as strings
from .choices import MapType

from .forms import UploadForm
# Create your views here.


@custom_login_required
@custom_permission_required('home.access_uploader', messages.WARNING, strings.NO_UPLOADER_ACCESS)
def uploader(request):

    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            selected = form.cleaned_data.get('servers')
            print(request.FILES)
            #map_type = form.fields['map_type'].choices[int(form.cleaned_data.get('map_type'))][1]
            print(selected)
        else:
            print(form.errors)

    form = UploadForm()
    return render(request, 'uploader.html', {'form': form})