from .models import UzsakymuAtsiliepimai, Profilis, Uzsakymas
from django import forms
from django.contrib.auth.models import User


class UzsakymuAtsiliepimaiForm(forms.ModelForm):
    class Meta:
        model = UzsakymuAtsiliepimai
        fields = ('atsiliepimas', 'uzsakymas', 'komentatorius')
        widgets = {'uzsakymas': forms.HiddenInput(), 'komentatorius': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateTimeInput):
    input_type = "date"


class VartotojoUzsakymuCreateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['automobilis', 'terminas', 'status']
        widgets = {'vartotojas': forms.HiddenInput(), 'terminas': DateInput()}