from django import forms
from django.core.exceptions import ValidationError


class ResizeImageForm(forms.Form):
    width = forms.CharField(label="Ширина", required=False)
    height = forms.CharField(label="Высота", required=False)

    def clean(self):
        cd = self.cleaned_data
        if not cd.get('width') and not cd.get('height'):
            raise ValidationError("Заполните хоть что-нибудь!")
        return cd


class NewImageForm(forms.Form):
    url = forms.URLField(label="Ссылка", required=False)
    image = forms.ImageField(label="Файл", required=False)

    def clean(self):
        cd = self.cleaned_data
        if cd.get('url') and cd.get('image'):
            raise ValidationError("Заполните только одно поле!")
        if not cd.get('url') and not cd.get('image'):
            raise ValidationError("Заполните хоть что-нибудь!")
        return cd
