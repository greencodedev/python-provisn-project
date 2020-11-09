from django.core.mail.message import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.utils.html import strip_tags

from .forms import *
from userdashboard.forms import CustomUserCreationForm
from userdashboard.models import Pricing_Fiat
from django.contrib import messages
from decimal import Decimal
from plutus.settings import SIGNUP_ENABLED
from userdashboard.accounts import UserMethods
from django.utils.timezone import timedelta


# Create your views here.
# Begin Frontpage Methods
def frontpage(request):
    # pricings = Pricing_Fiat.objects.filter(only_available_using_key=False)
    pricings_credit_card = Pricing_Fiat.objects.filter(show_on_page=True, only_available_using_key=False)
    pricings_crypto = []
    for price in pricings_credit_card:
        cost_eth = price.get_crypto_value(currency='ETH')
        cost_btc = price.get_crypto_value(currency='BTC')
        new_dict = {
            'cost': round(price.cost_cent * Decimal(10 ** -2)),
            'cost_ethereum': cost_eth if cost_eth else '',
            'cost_bitcoin': cost_btc if cost_btc else '',
            'subscription_time_in_days': price.subscription_time_in_days,
            'show_name': price.show_name,
            'id': price.id,
            'savings': price.saving,
        }
        pricings_crypto.append(new_dict)
    pricings_crypto = sorted(pricings_crypto, key=lambda k: k['subscription_time_in_days'])
    if request.method == 'POST':

        UCform = CustomUserCreationForm(request.POST)
        if 'UCform_Button' in request.POST:
            if UCform.is_valid():
                user = UCform.save(commit=False)
                user.is_active = False
                TokenObject = None
                if user.signup_token is not None and user.signup_token is not '':
                    from referral.models import Referral, SignedUpUserReferral
                    try:
                        TokenObject = Referral.objects.get(Token=user.signup_token)
                        TokenObject.AmountSignups += 1
                        TokenObject.save()

                    except Exception:
                        messages.error(request, 'Error with the entered referral token!')
                        return redirect(frontpage)

                user.save()
                if TokenObject is not None:
                    try:
                        ref_user_wrapper_object = SignedUpUserReferral(
                            RefToken=TokenObject,
                            User=user
                        )
                        ref_user_wrapper_object.save()
                        UserMethods.extendUserTrialByUserObject(user, timedelta(days=14))
                    except Exception:
                        messages.error(request, 'Error with the entered referral token!')
                        return redirect(frontpage)
                from django.contrib.sites.shortcuts import get_current_site
                current_site = get_current_site(request)
                mail_subject = 'Activate your Provisn.com account.'
                from django.utils.encoding import force_bytes
                from django.template.loader import render_to_string
                from django.utils.http import urlsafe_base64_encode
                from userdashboard.tokens import account_activation_token
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                text_content = strip_tags(message)
                to_email = UCform.cleaned_data.get('email')
                email = EmailMultiAlternatives(
                    mail_subject, text_content, to=[to_email]
                )
                email.attach_alternative(message, 'text/html')
                from smtplib import SMTPAuthenticationError
                try:
                    email.send()
                except SMTPAuthenticationError:
                    messages.error('An error occured when sending the confirmation mail! Please write a Support Ticker, thanks.')

                messages.success(request,
                                 "Successfully signed up! Please confirm your e-mail address to complete the registration!")
                MTAform = SupportTicketForm()
                return render(request, 'frontpage/main.html',
                              {'MTAform': MTAform, 'UCform': UCform, 'pricings': pricings_crypto, 'SIGNUP_ENABLED': SIGNUP_ENABLED})
            else:
                for error in UCform.errors.items():
                    messages.error(request, error[1])

    else:
        if 'reftoken' in request.GET:
            UCform = CustomUserCreationForm(initial={'signup_token': request.GET['reftoken']})
        else:
            UCform = CustomUserCreationForm()

    if request.method == 'POST' and 'MTAform_Button' in request.POST:
        MTAform = SupportTicketForm(request.POST)
        if UCform.is_valid():
            UCform.clean()
        if MTAform.is_valid():
            MTAform.save()
            messages.success(request, "The form has been sent successfully! We'll contact you as soon as possible.")
            return render(request, 'frontpage/main.html',
                          {'MTAform': MTAform, 'UCform': UCform, 'pricings': pricings_crypto, 'SIGNUP_ENABLED': SIGNUP_ENABLED})

    else:
        MTAform = SupportTicketForm()
        if 'reftoken' in request.GET:
            UCform = CustomUserCreationForm(initial={'signup_token': request.GET['reftoken']})
        else:
            UCform = CustomUserCreationForm()
    return render(request, 'frontpage/main.html', {'MTAform': MTAform, 'UCform': UCform, 'pricings': pricings_crypto, 'SIGNUP_ENABLED': SIGNUP_ENABLED})


# def frontpage_pricing(request):
#    return render(request, 'front_page/pricing.html')


# def frontpage_team(request):
#    return render(request, 'frontpage/team.html')


# def frontpage_about(request):
#    return render(request, 'front_page/about.html')


# def frontpage_how_it_works(request):
#    return render(request, 'front_page/how_it_works.html')


def frontpage_terms(request):
    return render(request, 'frontpage/terms.html')


def frontpage_privacy(request):
    return render(request, 'frontpage/privacy.html')


# Support Contact Form
# Also handles it saving
"""
def admin_contact(request):
    if request.method == "POST":
        form = MessageToAdminForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Form sent successfully.\nThanks, we'll  contact you as soon as possible.")
            return redirect('frontpage')
    else:
        form = MessageToAdminForm()
    return render(request, 'frontpage/contact.html', {'form': form})
# End Frontpage methods
"""
