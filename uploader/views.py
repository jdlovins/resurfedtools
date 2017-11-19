from django.shortcuts import render
from home.decorators import custom_login_required, custom_permission_required
from django.contrib import messages
import uploader.strings as strings

from .forms import UploadForm
# Create your views here.


@custom_login_required
@custom_permission_required('user.access_uploader', messages.WARNING, strings.NO_UPLOADER_ACCESS)
def uploader(request):
    form = UploadForm()
    return render(request, 'uploader.html', {'form': form})