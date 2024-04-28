from django.forms import ModelForm, Select

from .models import Location


class LocationForm(ModelForm):
    """
    Форма для выбора местоположения
    """
    class Meta:
        model = Location
        fields = ["name"]
        widgets = {
            'name': Select(),
        }
