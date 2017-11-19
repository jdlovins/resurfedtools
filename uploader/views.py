from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from home.decorators import custom_login_required
from .forms import UploadForm
# Create your views here.


@custom_login_required
def uploader(request):
    form = UploadForm()
    return render(request, 'uploader.html', {'form': form})