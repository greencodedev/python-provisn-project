from django.forms import ModelForm, DateInput
from userdashboard.models import BlockchainEvent as Event
from django import forms
from django.utils.safestring import mark_safe


class EventForm(ModelForm):

    COLOR_CHOICES = (
        ('event_color_brown', 'Coin Event (Brown)'),
        ('event_color_blue', 'Location Based Event (Blue)'),
        ('event_color_green', 'Provisn Event (Green)'),
    )

    color_class = forms.ChoiceField(choices=COLOR_CHOICES)
    title = forms.CharField(required=True)
    date_of_event = forms.DateTimeField(
        label_suffix=mark_safe('<small> (D/M/Y H:M <small>24H</small>)</small>'),
        input_formats=['%d/%m/%Y %H:%M',],
        required=True,
        widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Event
        fields = ['title', 'date_of_event', 'color_class', 'text', 'tags']
