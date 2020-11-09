import random
import string


def get_amount_days_current_month():
    import calendar, datetime
    now = datetime.datetime.now()
    return calendar.monthrange(now.year, now.month)[1]

def get_current_month_name():
    import datetime
    return datetime.datetime.now().strftime('%B')

def get_current_day():
    import datetime
    return datetime.datetime.now().strftime('%-d')

def payment_confirmation_mail(user, payment_amount, sub_time):
    from django.core.mail import send_mail
    try:
        send_mail(
            'Provisn.com Payment Successful',
            'Your Provisn.com Account has been successfully prolonged for ' + sub_time + ' days.\nThe paid amount was: ' + payment_amount,
            'payment@provisn.com',
            [user.email]
        )
    except Exception as exc:
        print('Error sending payment confirmation mail: ' + str(exc))


def update_news_article(instance):
    if instance.information_updated:
        if instance.title is None or instance.news_url is None:
            instance.delete()
        return
    from requests import Session
    from bs4 import BeautifulSoup
    try:
        str = instance.text
        soup = BeautifulSoup(str, 'html.parser')
        url = soup.find('a')['href']
        import urllib.parse
        url = urllib.parse.quote(url, safe='')

        app_id = 'bb47e7d7-c243-4285-a4ce-c31f00687756'
        get_url = 'https://opengraph.io/api/1.1/site/' + url + '?app_id=' + app_id

        parameters = {
            'app_id': 'f1c453c8-948f-4a7a-8c27-a5f3add9ce4b'
        }
        headers = {
            'Accepts': 'application/json',
            'app_id': 'f1c453c8-948f-4a7a-8c27-a5f3add9ce4b'
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(get_url, params=parameters)
        from json import loads
        data = loads(response.text)
        instance.title = data['hybridGraph']['title']
        instance.image_url = data['hybridGraph']['image']
        instance.information_updated = True
        instance.news_url = url
        instance.save()
    except Exception:
        instance.hidden = True
        instance.save()

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_currency_value(currency_id):
    from coinpaprika import client as CoinPaprika
    client = CoinPaprika.Client()
    data = client.ticker(currency_id)
    return data

def test_user_referral(mail_user):
    try:
        from userdashboard.models import CustomUser
        user = CustomUser.objects.get(email=mail_user)
        from referral.models import SignedUpUserReferral
        refToken = SignedUpUserReferral.objects.get(User=user).RefToken
        if not refToken.ReferralSubscribers.filter(email=user.email).exists():
            refToken.AmountReferrals += 1
            refToken.check_reward()
            refToken.ReferralSubscribers.add(user)
            refToken.save()
        else:
            error_msg = 'User referral has already been gifted'
            print(error_msg)
    except SignedUpUserReferral.DoesNotExist:
        pass
    except Exception:
        pass
