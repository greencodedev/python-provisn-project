from django import forms
from .models import OpenPayout


class OpenPayoutForm(forms.ModelForm):
    Holders_Name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'textfield-contact form_input', 'type': 'text', 'id': 'holders_name',
               'placeholder': 'HOLDERS NAME'}), required=True)
    Bank_Name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'textfield-contact form_input', 'type': 'text', 'id': 'bank_name',
               'placeholder': 'BANK NAME'}), required=True)
    IBAN = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'textfield-contact form_input', 'type': 'text', 'id': 'iban',
               'placeholder': 'IBAN'}), required=True)
    SWIFT = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'textfield-contact form_input', 'type': 'text', 'id': 'swift_code',
               'placeholder': 'SWIFT/BIC CODE'}), required=True)

    class Meta:
        model = OpenPayout
        fields = ('Holders_Name', 'Bank_Name', 'IBAN', 'SWIFT' )

