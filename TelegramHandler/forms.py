from django import forms
from django.utils.safestring import mark_safe

from .models import TelegramAccountWrapper


class CreateTelegramAccountForm(forms.ModelForm):
    telegram_name = forms.CharField(
        label='',
        label_suffix=mark_safe(
            '<p>Enter your Telegram name here:<br/><small>e.g. @DcPacky</small><br/></p>'
        ),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Telegram Name e.g. @MyName',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = TelegramAccountWrapper
        fields = ('telegram_name', )