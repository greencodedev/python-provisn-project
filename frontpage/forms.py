from django import forms
from .models import SupportTicket
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
#from captcha.fields import CaptchaField
#from ckeditor.widgets import CKEditorWidget

### This is the form for the SupportMessage Model
class SupportTicketForm(forms.ModelForm):
    captcha = ReCaptchaField(label='')
    byName = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={'class': 'textfield-contact', 'name': 'byName', 'type': 'text', 'id': 'byName',
               'placeholder': 'Name'}), required=False)
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea_styled', 'name': 'text', 'type': 'text', 'id': 'text',
               'placeholder': 'Enter your message here'}), required=False)
    email_ticket = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'textfield-contact', 'name': 'email', 'type': 'email', 'id': 'email',
               'placeholder': 'E-Mail'}), required=True)
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'textfield-contact', 'name': 'phone_number', 'type': 'tel', 'id': 'phone_number',
               'placeholder': 'Phone Number'}), required=False)

    class Meta:
        model = SupportTicket
        fields = ('byName', 'email_ticket', 'phone_number', 'text', 'captcha')