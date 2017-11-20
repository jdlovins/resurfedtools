from django import forms
from .models import Server
from .choices import MapType
from django.utils.safestring import mark_safe


class UploadForm(forms.Form):
    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    servers = forms.ModelMultipleChoiceField(queryset=Server.objects.none(), widget=forms.CheckboxSelectMultiple)

    # replace_map = forms.BooleanField()

    insert_map_info = forms.BooleanField(
        initial=False,
        help_text="Insert map info on upload?",
        required=False
    )

    map_author = forms.CharField(
        max_length=32,
        help_text="Name of the map maker, duh.",
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Big Blue',
                'class': 'form-control',
                'tabindex': 2,
                'disabled': True,
            }
        )
    )

    map_tier = forms.IntegerField(
        min_value=1,
        max_value=6,
        help_text="Tier of the map, choose carefully!",
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 3,
                'disabled': True
            }
        )
    )

    map_type = forms.ChoiceField(
        choices=((0, "Staged"),
                 (1, "Linear")),
        required=False,
        widget=forms.Select(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 4,
                'disabled': True
            }
        )
    )

    map_zones = forms.IntegerField(
        min_value=1,
        max_value=32,
        help_text=mark_safe("Staged maps = Stages <br/> Linear maps = checkpoints + 1 <br/> "
                            "Linear maps must have at least 1 checkpoint!"),
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 5,
                'disabled': True,
                'size': 10
            }
        )
    )

    map_bonuses = forms.IntegerField(
        min_value=1,
        max_value=32,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 1,
                'class': 'form-control',
                'tabindex': 6,
                'disabled': True
            }
        )
    )

    disable_pre_hop = forms.BooleanField(
        initial=False,
        required=False,
        help_text="Disable prehopping"
    )

    enable_baked_triggers = forms.BooleanField(
        initial=False,
        required=False,
        help_text="Enabled baked in triggers"
    )

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)

        self.fields['servers'].queryset = Server.objects.all()
