from django import forms

from django_samba_ad.core.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []
        widgets = {
            'username': forms.HiddenInput
        }