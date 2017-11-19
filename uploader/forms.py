from django import forms
from .models import Server


class UploadForm(forms.Form):

    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    servers = forms.ModelMultipleChoiceField(queryset=Server.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)

        self.fields['servers'].queryset = Server.objects.all()