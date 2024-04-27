from django.forms import ModelForm, Select

from .models import Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ["name"]
        widgets = {
            'name': Select(),
        }
