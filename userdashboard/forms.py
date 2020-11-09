from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from captcha.fields import ReCaptchaField
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagField, TagWidget
from django.utils.safestring import mark_safe


### Forms file, provides forms for either the website itself e.g. the Support Message form
### or the admin page e.g. PaymentForm
### It also provides the custom fields for the registration of the CustomUser Model

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form_input', 'name': 'username', 'type': 'username', 'id': 'subs-username',
               'placeholder': 'Username'}), required=False)
    email = forms.EmailField(label="E-Mail", required=False, widget=forms.TextInput(
        attrs={'class': 'form_input', 'name': 'email', 'type': 'email', 'id': 'subs-email',
               'placeholder': 'E-Mail'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form_input', 'name': 'password', 'type': 'password', 'id': 'subs-password',
               'placeholder': 'Password'}), required=False)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form_input', 'name': 'password2', 'type': 'password', 'id': 'subs-password-2',
               'placeholder': 'Password Confirmation'}), required=False)
    signup_token = forms.CharField(label='Referral Token', widget=forms.TextInput(
        attrs={
            'placeholder': 'Referral Token (Optional)', 'type': 'text', 'class': 'form_input'
        }
    ), required=False)
    #captcha = CaptchaField(required=False)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',  'signup_token')


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'sr-only'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class PaymentForm_Crypto(forms.ModelForm):
    class Meta:
        model = Payment_Crypto
        fields = ('coin', 'value', 'browser_request')


class BugReportForm(forms.ModelForm):
    captcha = ReCaptchaField()
    title = forms.CharField(label='Topic', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Title'}))
    regard = forms.CharField(label='Please Specify which page or parts of the website this report is about', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Website location'}))
    email = forms.CharField(label='E-Mail (Will be used in case we have questions)', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'email', 'type': 'email', 'id': 'email',
               'placeholder': 'E-Mail'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control input-lg', 'name': 'text', 'type': 'text', 'id': 'text',
               'placeholder': 'Enter your text here', 'style': 'min-height:250px;'}))


    class Meta:
        model = BugReport
        fields = ('title', 'email', 'regard', 'text' )



### Content Creation Forms

BEAMS_COLORS = [
    ('beam-btc', 'BTC Pair'),
    ('beam-eth', 'ETH Pair'),
    ('beam-fiat', 'FIAT Pair'),
    ('beam-other', 'Other Pair'),
]

EXCHANGE_NAMES = (
    ('Binance', 'Binance'),
    ('CoinBase', 'CoinBase'),
    ('Kraken', 'Kraken'),
    ('Upbit', 'Upbit'),
    ('Huobi', 'Huobi'),
    ('Bittrex', 'Bittrex'),
    ('Bithumb', 'Bithumb'),
    ('OKEx', 'OKEx'),
    ('Bitfinex', 'Bitfinex'),
    ('Bitstamp', 'Bitstamp'),
    ('KuCoin', 'KuCoin'),
)

class BeamsForm(forms.ModelForm):
    pair = forms.CharField(label='Pair', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Title'}))
    tags = TagField(
        label_suffix=mark_safe('<br/><small style="">Add Comma separated tags here</small>'),
        widget=TagWidget(attrs={'class': 'form-control input-lg', 'placeholder': 'Tags'}), required=False)

    entry = forms.Field(label='Entry', widget=forms.Textarea(attrs={'style': 'width:100%;', 'rows':'3'}))
    targets = forms.Field(label='Targets', widget=forms.Textarea(attrs={'style': 'width:100%;', 'rows': '3'}))
    stop_loss = forms.Field(label='Stop Loss', widget=forms.Textarea(attrs={'style': 'width:100%;', 'rows': '3'}))
    exchange = forms.CharField(label='Exchange', widget=forms.Select(choices=EXCHANGE_NAMES))
    color_class = forms.CharField(label='Beam Color', widget=forms.Select(choices=BEAMS_COLORS))

    class Meta:
        model = Beam
        fields = ('pair', 'tags', 'entry', 'targets', 'stop_loss', 'exchange', 'color_class')


class BlockchainEventForm(forms.ModelForm):
    title = forms.CharField(label='Topic', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Title'}))
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Beam
        fields = ('title', 'text',)

class BlockchainNewsForm(forms.ModelForm):
    title = forms.CharField(label='Topic', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Title'}))
    text = forms.CharField(widget=CKEditorWidget())
    tags = TagField(
        label_suffix=mark_safe('<br/><small style="margin-top:450px;">Add Comma separated tags here</small>'),
        widget=TagWidget(attrs={'class': 'form-control input-lg', 'placeholder': 'Tags'}), required=False)
    class Meta:
        model = BlockchainNew
        fields = ('title', 'tags', 'text',)

class ArtificialIntelligenceForm(forms.ModelForm):
    title = forms.CharField(label='Topic', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Title'}))
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ArtificialIntelligence
        fields = ('title', 'text',)


class TechnicalAnalysisForm(forms.ModelForm):
    title = forms.CharField(label='Topic', widget=forms.TextInput(
        attrs={'class': 'form-control input-lg', 'name': 'title', 'type': 'text', 'id': 'title',
               'placeholder': 'Title'}))
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = TechnicalAnalysi
        fields = ('title', 'tags', 'text', 'notes', 'url', 'image_url')


class TokenWatchlistForm(forms.ModelForm):
    About = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = TokenWatchlist
        fields = (
            'coin',
            'coin_icon',
            'tags',
            'About',
            'Product',
            'Team',
            'Value',
        )



class BeamCommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your text here...', 'rows': 4,
                   'maxlength': '256', 'data-limit-rows': 'true', 'id': 'chatInputText', 'style': 'min-height:250px;', 'type': 'text'})
    )
    class Meta:
        model = BeamsComment
        fields = ('text',)

class BlockchainNewsCommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your text here...', 'rows': 4,
                   'maxlength': '256', 'data-limit-rows': 'true', 'id': 'chatInputText', 'style': 'min-height:250px;', 'type': 'text'})
    )
    class Meta:
        model = BlockchainNewsComment
        fields = ('text',)

class BlockchainEventCommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your text here...', 'rows': 4,
                   'maxlength': '256', 'data-limit-rows': 'true', 'id': 'chatInputText', 'style': 'min-height:250px;', 'type': 'text'})
    )
    class Meta:
        model = BlockchainEventsComment
        fields = ('text',)

class AICommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your text here...', 'rows': 4,
                   'maxlength': '256', 'data-limit-rows': 'true', 'id': 'chatInputText', 'style': 'min-height:250px;', 'type': 'text'})
    )
    class Meta:
        model = ArtificialIntelligenceComment
        fields = ('text',)

class TACommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your text here...', 'rows': 4,
                   'maxlength': '256', 'data-limit-rows': 'true', 'id': 'chatInputText', 'style': 'min-height:250px;', 'type': 'text'})
    )
    class Meta:
        model = TechnicalAnalysisComment
        fields = ('text',)

class TWCommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'class': 'form-control input-lg', 'placeholder': 'Enter your text here...', 'rows': 4,
                   'maxlength': '256', 'data-limit-rows': 'true', 'id': 'chatInputText', 'style': 'min-height:250px;', 'type': 'text'})
    )
    class Meta:
        model = TokenWatchlistComment
        fields = ('text',)
