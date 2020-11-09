from itertools import chain

import stripe
from django.views.decorators.csrf import csrf_exempt
from plutus import settings
from .forms import *
import userdashboard.models as ud_models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator
from cryptapi import Invoice as cryptapi_invoice

import sys
import csv
from cryptapi.models import Request as cryptapi_request
from django.core.exceptions import ObjectDoesNotExist
from TelegramHandler.models import TelegramAccountWrapper, ContentCoinDesk
from ContentScraper.models import *
from .utils import get_amount_days_current_month, get_current_month_name, get_current_day
import json

sys.path.append("..")

### CHANGE IMPORTANT VARIABLES HERE
AMOUNT_ROUNDTABLE_MESSAGES_DASHBOARD = 5
AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE = 16
AMOUNT_TA_PER_PAGE = 32

CURRENTVERSION = '1.0'

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLISHABLE_KEY

DEBUG = settings.DEBUG


# Helper Functions
# Grabbing the discord data from the pkl files and returning dicts to the views
# First function is for the dashboard and the second for the content pages
# Dashboard function only return one element in a list of dictionaries
def isUserSubscribedByRequest(request):
    return request.user.userLevel == 1 \
           or request.user.userLevel == 2 \
           or request.user.userLevel == 3 \
           or request.user.userLevel == 4


# Print text for user subscription has run out function
def printUserSubscriptionHasRunOut(request):
    messages.error(request,
                   "Your subscription has run out, Subscribe today! Below you'll find the options needed to refresh it.")


# The real views begin here, update those to change answers to the user browser or change website appearance

# Creates objects using the dashboard function above and passes them to the view where they'll be displayed in those boxes
@login_required
def userDashboard(request):
    from itertools import chain
    Title = "Your Dashboard"
    subHeader = 'Latest and Greatest in the Blockchain world.'
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    try:
        beams = Beam.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        beams = list(chain(beams))
        beams = sorted(beams)[:4]

        events = BlockchainEvent.objects.filter(date_of_event__gte=timezone.now()).order_by('date_of_event')[:3]
        from django.core import serializers
        events = serializers.serialize('json', events)

        news = BlockchainNew.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        coindesk = ContentCoinDesk.objects.all().order_by('-published_date')
        news = list(chain(news, coindesk))
        news = sorted(news)[:8]

        ai = ArtificialIntelligence.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:6]

        technical_analysis = TechnicalAnalysi.objects.filter(published_date__lte=timezone.now()).order_by(
            '-published_date')

        faibik_content = Content_Faibik.objects.filter(hidden=False).order_by('-published_date')
        khaled_abdulaziz_content = Content_KhaledAbdulaziz.objects.filter(hidden=False).order_by('-published_date')
        alanmasters_content = Content_alanmasters.objects.filter(hidden=False).order_by('-published_date')
        cryptontez_content = Content_CryptoNTez.objects.filter(hidden=False).order_by('-published_date')

        technical_analysis = list(chain(technical_analysis,
                                        cryptontez_content,
                                        faibik_content,
                                        khaled_abdulaziz_content,
                                        alanmasters_content,
                                        ))
        technical_analysis = sorted(technical_analysis)[:3]

        token_watchlist = TokenWatchlist.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[
                          :3]

        coins = Coin.objects.all()[:10]

        fear_and_greed = Fear_and_Greed_Index.objects.latest('update_time') or ''

    except ObjectDoesNotExist:
        response = render(request, 'user_area/user/dashboard.html', {
            'navId': 'dashboardNavLink',
            'pagetitle': Title,
            'subHeader': subHeader,
            'dashboard': True,
            'coins': coins,
            'fear_and_greed': fear_and_greed
        })
        return response

    response = render(request, 'user_area/user/dashboard.html', {
        'beams': beams,
        'events': events,
        'news': news,
        'plutus_ai': ai,
        'technical_analysis': technical_analysis,
        'token_watchlist': token_watchlist,
        'navId': 'dashboardNavLink',
        'pagetitle': Title,
        'subHeader': subHeader,
        'dashboard': True,
        'days_current_month': get_amount_days_current_month(),
        'current_month_name': get_current_month_name(),
        # 'current_day': get_current_day(),
        'current_day': '15',
        'fear_and_greed': fear_and_greed,
    })
    return response


# All of the following functions are for the content pages and are the same except for the roundtable
# Begin user member area methods
@login_required
def userBeams(request):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    beams = Beam.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    beams = list(chain(beams))
    beams = sorted(beams)

    paginator = Paginator(beams, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    beams = paginator.get_page(page)
    Title = "Beams"
    subHeader = "Robust, dependable, and comprehensive signal calls"
    PageRefAddContent = 'NewBeams'

    response = render(request, 'user_area/user/Content_Pages/Beams.html', {
        'items': beams,
        'pagetitle': Title,
        'navId': 'beamsNavLink',
        'subHeader': subHeader,
        'PageRefAddContent': PageRefAddContent
    })
    return response


@login_required
def userBlockchainEvents(request):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    # events = createContentPageObject('blockchain_events')
    events = BlockchainEvent.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(events, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    Title = "Calendar"
    subHeader = "Choice upcoming blockchain events"
    PageRefAddContent = 'NewBlockchainEvents'

    response = render(request, 'user_area/user/Content_Pages/Events.html',
                      {'items': events, 'pagetitle': Title, 'navId': 'eventsNavLink', 'subHeader': subHeader,
                       'PageRefAddContent': PageRefAddContent})
    return response


from TwitterHandler.models import Tweet


@login_required
def userNews(request):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)

    news = BlockchainNew.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # tweets = Tweet.objects.all().order_by('-published_date')
    coindesk = ContentCoinDesk.objects.all().order_by('-published_date')
    news = list(chain(news, coindesk))
    news = sorted(news)

    paginator = Paginator(news, 74)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    Title = "News"
    subHeader = "Curated on-demand news directly from vetted resources"
    PageRefAddContent = 'NewBlockchainNews'
    response = render(request, 'user_area/user/Content_Pages/News.html', {
        'items': news,
        'pagetitle': Title,
        'navId': 'newsNavLink',
        'subHeader': subHeader,
        'PageRefAddContent': PageRefAddContent,
        'coindesk': coindesk,
    })
    return response


@login_required
def userAI(request):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    ai = ArtificialIntelligence.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(ai, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    ai = paginator.get_page(page)
    Title = "AI Signal Calls"
    subHeader = "Advanced AI and crowd-sourced marked modeling agents"
    navId = 'aiNavLink'
    PageRefAddContent = 'NewAI'

    response = render(request, 'user_area/user/Content_Pages/AI.html',
                      {'items': ai, 'pagetitle': Title, 'navId': navId, 'subHeader': subHeader,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def userTechnicalAnalysis(request):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    # technicalAnalysis = createContentPageObject('technical_analysis')
    technicalAnalysis = TechnicalAnalysi.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    faibik_content = Content_Faibik.objects.filter(hidden=False).order_by('-published_date')
    khaled_abdulaziz_content = Content_KhaledAbdulaziz.objects.filter(hidden=False).order_by('-published_date')
    alanmasters_content = Content_alanmasters.objects.filter(hidden=False).order_by('-published_date')
    cryptontez_content = Content_CryptoNTez.objects.filter(hidden=False).order_by('-published_date')

    from itertools import chain
    technicalAnalysis = list(chain(technicalAnalysis,
                                   faibik_content,
                                   khaled_abdulaziz_content,
                                   alanmasters_content,
                                   cryptontez_content
                                   ))
    technicalAnalysis = sorted(technicalAnalysis)

    paginator = Paginator(technicalAnalysis, AMOUNT_TA_PER_PAGE)
    page = request.GET.get('page')
    technicalAnalysis = paginator.get_page(page)
    Title = "Technical Analysis"
    subHeader = "Critical updates on key market trends and cryptos"
    PageRefAddContent = 'NewTA'

    response = render(request, 'user_area/user/Content_Pages/Technical-Analysis.html',
                      {'items': technicalAnalysis, 'pagetitle': Title, 'navId': 'technicalAnalysisNavLink',
                       'subHeader': subHeader, 'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def userTokenWatchlist(request):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    # tokenWatchlist = createContentPageObject('token_watchlist')
    tokenWatchlist = TokenWatchlist.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(tokenWatchlist, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    tokenWatchlist = paginator.get_page(page)
    Title = "Token Spotlight"
    subHeader = "Exploration of upcoming technologies, projects, and events"
    PageRefAddContent = 'NewTW'

    response = render(request, 'user_area/user/Content_Pages/Token-Watchlist.html',
                      {'items': tokenWatchlist, 'pagetitle': Title, 'navId': 'tokenWatchlistNavLink',
                       'subHeader': subHeader, 'PageRefAddContent': PageRefAddContent})
    return response


@staff_member_required
def userAdminTools(request):
    if not (request.user.is_staff):
        messages.error("You are not allowed to enter this area!")
        return redirect(member)
    Title = "Staff Tools"
    subHeader = "Here you'll find useful tools for administrative purposes"

    response = render(request, 'user_area/user/admin_tools.html',
                      {'pagetitle': Title, 'navId': 'adminToolsNavLink', 'subHeader': subHeader})
    return response


@login_required
def userSettings(request):
    isStaff = False
    if (request.user.is_staff):
        isStaff = True
    Title = "Settings"
    subHeader = "Configure Provisn the way you like!"
    SupportTickets = None
    BugReports = None
    if isStaff:
        from frontpage.models import SupportTicket
        OpenSupportTickets = SupportTicket.objects.filter(status='OPEN')
        BugReports = BugReport.objects.filter(status='OPEN')
    else:
        OpenSupportTickets = []

    if OpenSupportTickets is None and BugReports is None:
        response = render(request,
                          'user_area/user/settings.html',
                          {
                              'pagetitle': Title,
                              'isStaff': isStaff,
                              'subHeader': subHeader,
                              'currentversion': CURRENTVERSION
                          })
    elif OpenSupportTickets is None:
        response = render(request,
                          'user_area/user/settings.html',
                          {
                              'pagetitle': Title,
                              'isStaff': isStaff,
                              'subHeader': subHeader,
                              'AmountOpenBugReports': len(BugReports) or None,
                              'currentversion': CURRENTVERSION
                          })
    elif BugReports is None:
        response = render(request,
                          'user_area/user/settings.html',
                          {
                              'pagetitle': Title,
                              'isStaff': isStaff,
                              'subHeader': subHeader,
                              'AmountOpenSupportTickets': len(OpenSupportTickets) or None,
                              'currentversion': CURRENTVERSION
                          })
    else:
        response = render(request,
                          'user_area/user/settings.html',
                          {
                              'pagetitle': Title,
                              'isStaff': isStaff,
                              'subHeader': subHeader,
                              'AmountOpenSupportTickets': len(OpenSupportTickets) or None,
                              'AmountOpenBugReports': len(BugReports) or None,
                              'currentversion': CURRENTVERSION
                          })
    return response


@login_required
def search(request):
    if request.method == 'GET':

        query = request.GET.get('q')
        submit_button = request.GET.get('submit')

        Title = 'Search Results for "' + query + '"'
        subHeader = 'You searched for ' + query

        if query is not None:
            lookups = Q(title__icontains=query) | Q(text__icontains=query) | Q(tags__name=query)
            lookups_tw = Q(About__icontains=query) | Q(Product__icontains=query) | Q(Team__icontains=query) | Q(
                Value__icontains=query) | Q(tags__name=query)
            lookup_beams = Q(pair__icontains=query) | Q(exchange__icontains=query) | Q(tags__name=query)
            lookup_ai = Q(text__icontains=query) | Q(tags__name=query)
            lookup_scraped_ta = Q(title__icontains=query) | Q(text__icontains=query)

            resultsBeam = Beam.objects.filter(published_date__lte=timezone.now()).filter(lookup_beams).distinct()
            resultsEvents = BlockchainEvent.objects.filter(published_date__lte=timezone.now()).filter(
                lookups).distinct()
            resultsNews = BlockchainNew.objects.filter(published_date__lte=timezone.now()).filter(lookups).distinct()
            resultsAI = ArtificialIntelligence.objects.filter(published_date__lte=timezone.now()).filter(
                lookup_ai).distinct()
            resultsTW = TokenWatchlist.objects.filter(published_date__lte=timezone.now()).filter(lookups_tw).distinct()

            # Telegram Results
            results_coin_desk = ContentCoinDesk.objects.filter(Q(title__icontains=query)).distinct()

            resultsTA = TechnicalAnalysi.objects.filter(published_date__lte=timezone.now()).filter(lookups).distinct()
            resultsTA_F = Content_Faibik.objects.filter(published_date__lte=timezone.now()).filter(lookup_scraped_ta).distinct()
            resultsTA_KA = Content_KhaledAbdulaziz.objects.filter(published_date__lte=timezone.now()).filter(lookup_scraped_ta).distinct()
            resultsTA_AM = Content_alanmasters.objects.filter(published_date__lte=timezone.now()).filter(lookup_scraped_ta).distinct()
            resultsTA_NT = Content_CryptoNTez.objects.filter(published_date__lte=timezone.now()).filter(lookup_scraped_ta).distinct()

            from itertools import chain
            import operator
            results = chain(
                resultsBeam,
                resultsEvents,
                resultsNews,
                resultsAI,
                resultsTW,

                results_coin_desk,

                resultsTA,
                resultsTA_AM,
                resultsTA_F,
                resultsTA_KA,
                resultsTA_NT
            )
            results = sorted(results, key=operator.attrgetter('published_date'))[::-1]
            # results = resultsBeam | resultsEvents | resultsNews | resultsMarketIntuition | resultsMemberPerks | resultsAI | resultsTA | resultsTW

            context = {
                'items': results,
                'submit_button': submit_button,
                'pagetitle': Title,
                'subHeader': subHeader,
                'searchPage': True
            }
            return render(request, 'user_area/user/Content_Pages/Search.html', context)

        else:
            return render(request, 'user_area/user/Content_Pages/Search.html')
    else:
        return render(request, 'user_area/user/Content_Pages/Search.html')


@staff_member_required
def userChangelog(request):
    if not (request.user.is_staff):
        messages.error("You are not allowed to enter this area!")
        return redirect(member)
    Title = "Changelog"
    subHeader = "Get informed about the newest Provisn updates!"
    ChangeObjects = ChangeLog.objects.all()
    paginator = Paginator(ChangeObjects, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    ChangeObjects = paginator.get_page(page)

    response = render(request, 'user_area/user/ContentListPage.html',
                      {'pagetitle': Title, 'subHeader': subHeader, 'items': ChangeObjects})
    return response


# Transforms the user level into understandable text and sends users the member page
from TelegramHandler.forms import CreateTelegramAccountForm


@login_required
def member(request):
    if request.method == 'POST':
        form = CreateTelegramAccountForm(request.POST)
        if 'payment_value_eth' in request.session:
            del request.session['payment_value_eth']
        if 'payment_value_btc' in request.session:
            del request.session['payment_value_btc']
        if 'coupon_value' in request.session:
            del request.session['coupon_value']
        if 'coupon_value_btc' in request.session:
            del request.session['coupon_value_btc']

        if 'payment_value_eth' in request.POST:
            request.session['payment_value_eth'] = request.POST['payment_value_eth']
            return HttpResponseRedirect('payment/')
        if 'payment_value_btc' in request.POST:
            request.session['payment_value_btc'] = request.POST['payment_value_btc']
            return HttpResponseRedirect('payment/')
        if 'coupon_value' in request.POST:
            request.session['coupon_value'] = request.POST['coupon_value']
            return HttpResponseRedirect('payment/')
        if 'coupon_value_btc' in request.POST:
            request.session['coupon_value_btc'] = request.POST['coupon_value_btc']
            return HttpResponseRedirect('payment/')
        if 'payment_value_credit_card' in request.POST:
            return credit_card_payment_charge(request)

        if form.is_valid():
            model = form.save(commit=False)
            model.account = request.user
            model.save()
            return redirect(member)

    Title = "Your Provisn Account"
    userLvl = request.user.userLevel
    userRank = ""
    if userLvl == 0:
        userRank = "Unsubscribed"
    elif userLvl == 1:
        userRank = "Trial"
    elif userLvl == 2:
        userRank = "Subscriber"
    elif userLvl == 3:
        userRank = "Lifetime"
    elif userLvl == 4:
        userRank = "Administrator"
    time_left = ""
    if request.user.sub_until > timezone.now():
        time_left = request.user.sub_until - timezone.now()
        time_left = time_left.days

    payment_history_objects = Payment_Crypto.objects.filter(user=request.user)
    payment_history_crypto_currency = []
    from cryptapi.models import Request as cryptapi_request
    for payment in payment_history_objects:
        test = (payment.pk + 1)
        try:
            payment_request = cryptapi_request.objects.get(order_id=(payment.pk + 1))
            obj = {}
            obj['package'] = payment.pricing.show_name
            obj['date_bought'] = payment_request.timestamp
            obj['status'] = payment_request.status
            obj['pk'] = payment.auto_increment_id
            payment_history_crypto_currency.append(obj)
        except (ObjectDoesNotExist, AttributeError):
            pass
    payment_history_objects = Payment_Fiat.objects.filter(user=request.user)
    invoices = ud_models.Invoice.objects.filter(user=request.user)

    from referral.utils import getUserReferralToken
    refToken = getUserReferralToken(request.user)

    createForm = False
    try:
        obj = TelegramAccountWrapper.objects.get(account=request.user)
        t_id = obj.telegram_name

    except Exception:
        createForm = True
    if createForm:
        tgform = CreateTelegramAccountForm()

    pricings_credit_card_objects = Pricing_Fiat.objects.filter(show_on_page=True, only_available_using_key=False)
    pricings_credit_card = []
    pricings_crypto = []
    for price in pricings_credit_card_objects:
        cost_btc = price.get_crypto_value(currency='BTC')
        cost_eth = price.get_crypto_value(currency='ETH')
        new_dict = {

            'cost_ethereum': cost_eth if cost_eth else '',
            'cost_bitcoin': cost_btc if cost_btc else '',
            'subscription_time_in_days': price.subscription_time_in_days,
            'show_name': price.show_name,
            'id': price.id,
            'savings': price.saving,
            'cost': round(price.cost_cent * 10**-2)
        }
        pricings_crypto.append(new_dict)
        new_dict = {
            'cost_cent': price.cost_cent,
            'subscription_time_in_days': price.subscription_time_in_days,
            'show_name': price.show_name,
            'stripe_recurring_plan': price.stripe_recurring_plan,
            'recurring_only': price.recurring_only,
            'savings': price.get_saving(),
            'cost': round(price.cost_cent * 10 ** -2)
        }
        pricings_credit_card.append(new_dict)

    pricings_credit_card = sorted(pricings_credit_card, key=lambda k: k['subscription_time_in_days'])
    pricings_crypto = sorted(pricings_crypto, key=lambda k: k['subscription_time_in_days'])

    is_subscribed = False
    try:
        sub = ActiveSubscription.objects.get(user=request.user)
        is_subscribed = True
    except Exception:
        pass
    except ObjectDoesNotExist:
        pass


    try:
        return render(request, 'user_area/user/member.html',
                      {
                          'pagetitle': Title,
                          'userRank': userRank, 'sub_since': request.user.sub_since,
                          'sub_until': request.user.sub_until,
                          'days_left': time_left,
                          'memberPage': True,
                          'telegramForm': tgform,
                          'refToken': refToken,
                          'payment_history_cryptocurrency': payment_history_crypto_currency,
                          'payment_history_creditcard': payment_history_objects,
                          'pricings': pricings_crypto,
                          'pricings_credit_card': pricings_credit_card,
                          'invoices': invoices,
                          'is_subscribed': is_subscribed
                      })
    # If user has no subscription the return above will throw an AttributeError
    except AttributeError as exc:
        print('Member Page Exception: ' + str(exc))
        return render(request, 'user_area/user/member.html',
                      {
                          'pagetitle': Title,
                          'userRank': userRank, 'sub_since': request.user.sub_since,
                          'sub_until': request.user.sub_until,
                          'days_left': time_left,
                          'memberPage': True,
                          'telegramForm': tgform,
                          'refToken': refToken,
                          'pricings': pricings_crypto,
                          'pricings_credit_card': pricings_credit_card,
                          'invoices': invoices,
                          'is_subscribed': is_subscribed
                      })
    except UnboundLocalError as exc:
        print('Member Page Exception: ' + str(exc))
        return render(request, 'user_area/user/member.html',
                      {
                          'pagetitle': Title,
                          'userRank': userRank, 'sub_since': request.user.sub_since,
                          'sub_until': request.user.sub_until,
                          'days_left': time_left,
                          'memberPage': True,
                          'refToken': refToken,
                          'pricings': pricings_crypto,
                          'pricings_credit_card': pricings_credit_card,
                          'invoices': invoices,
                          'is_subscribed': is_subscribed
                      })


@login_required
def credit_card_payment_charge(request):
    pricing = Pricing_Fiat.objects.get(cost_cent=request.POST['payment_value_credit_card'])
    if 'subscription' in request.POST:
        if pricing.is_recurring() is False:
            messages.error(request,
                           'This package is not available for recurring payments currently! Please contact our support for more information')
            return redirect(member)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            subscription_data={
                'items': [{
                    'plan': pricing.stripe_recurring_plan,
                }],
            },
            # line_items=[{
            #    'amount': pricing.cost_cent,
            #    'currency': 'usd',
            #    'name': 'Provisn Subscription',
            #    'description': 'Provisn Subscription for N months',
            #    'quantity': 1,
            # }],
            mode='subscription',
            success_url='https://dcpacky.space/provisn_test/member/account/paymentc/success' if DEBUG else 'https://provisn.com/member/account/paymentc/success',
            cancel_url='https://dcpacky.space/provisn_test/member/account/paymentc/cancelled' if DEBUG else 'https://provisn.com/member/account/paymentc/cancelled'
        )
    else:
        return
        if pricing.recurring_only:
            messages.error(request,
                           'This package can not be used for one time purchases currently! Please contact our support for more information')
            return redirect(member)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            line_items=[{
                'name': 'Provisn.com',
                'description': 'Access to your Crypto Currency Dashboard',
                'images': ['https://provisn.com/static/img/logo_black_bg.webp'],
                'amount': pricing.cost_cent,
                'currency': 'usd',
                'quantity': 1,
            }],
            success_url='https://dcpacky.space/provisn_test/member/account/paymentc/success' if DEBUG else 'https://provisn.com/member/account/paymentc/success',
            cancel_url='https://dcpacky.space/provisn_test/member/account/paymentc/cancelled' if DEBUG else 'https://provisn.com/member/account/paymentc/cancelled'
        )
    payment = Payment_Fiat(
        session_id=session.stripe_id,
        user=request.user,
        payment_amount=pricing.cost_cent,
        pricing=pricing,
        requested_at=timezone.now()
    )
    payment.save()
    response = render(request,
                      'user_area/user/payment_pages/card_charge.html',
                      {
                          'CHECKOUT_SESSION_ID': session.stripe_id,
                          'STRIPE_PUB': STRIPE_PUBLIC_KEY
                      })
    return response

@login_required
def credit_card_payment_charge_successful(request):
    return render(request, 'user_area/user/payment_pages/card_charge_success.html')

@login_required
def credit_card_payment_charge_cancelled(request):
    return render(request, 'user_area/user/payment_pages/card_charge_cancelled.html')


# End of user member area methods
@login_required
def send_friend_invitation(request):
    """View to show friend invitation window
    """
    from referral.models import Referral
    ref_token = Referral.objects.get(User=request.user).Token
    print(ref_token)
    if request.method == 'POST':
        ...
    return render(request, 'user_area/user/FriendInviter.html', {'token': ref_token})


from django.http.response import HttpResponse, HttpResponseRedirect


def signup(request):
    from django.utils.http import urlsafe_base64_encode
    from django.template.loader import render_to_string
    from .tokens import account_activation_token
    from django.core.mail import EmailMessage
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            if user.signup_token is not None or user.signup_token is not '':
                from referral.models import Referral
                try:
                    TokenObject = Referral.objects.get(Token=user.signup_token)
                    TokenObject.AmountReferrals += 1
                    TokenObject.check_reward()
                    TokenObject.save()
                    print(TokenObject)
                except Exception:
                    pass

            user.save()
            from django.contrib.sites.shortcuts import get_current_site
            ## ToDo: Fix domain in mails!
            current_site = get_current_site(request)
            mail_subject = 'Activate your Provisn.com account.'
            from django.utils.encoding import force_bytes
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_text
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    from userdashboard.tokens import account_activation_token
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        from frontpage.views import frontpage
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect(frontpage)
        # login(request, user)
        # return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def test_activated_page(request):
    return render(request, 'registration/activated.html')


# Sends default django logout request
def logOut(request):
    logout(request)
    response = redirect('/')
    messages.success(request, "Successfully logged out! See you later.")
    return response


# Hot topic following, please don't change anything more than the coin variable of the form object
# The value is derived from the url passing
@login_required
def order_creation_view(request, **kwargs):
    if 'order_id' in request.GET:
        # from cryptapi.models import Request as cryptapi_request
        # cryptapi_request.objects.get(order_id=request.GET['order_id'])

        response = render(request, 'user_area/user/payment.html', {})
        return response

    if 'coupon_value' in request.session or 'coupon_value_btc' in request.session:
        if DEBUG:
            print('Found coupon, trying to verify...!')
        coupon = request.session['coupon_value'] if 'coupon_value' in request.session else request.session[
            'coupon_value_btc']
        try:
            pricing = Pricing_Fiat.objects.get(key=coupon)
            valid = True
            try:
                ud_models.UsedCoupon.objects.get(coupon=pricing, user=request.user)
                valid = False
            except ObjectDoesNotExist:
                pass

            if valid is False:
                messages.error(request, 'Coupon has already been used.')
                return redirect(member)

            if pricing.is_free:
                try:
                    coupon = ud_models.UsedCoupon(
                        user=request.user,
                        coupon=pricing
                    )
                    coupon.save()
                except:
                    pass
                from userdashboard.accounts import UserMethods
                UserMethods.prolongUserSubscriptionByUserObject(request.user, timezone.timedelta(
                    days=pricing.subscription_time_in_days))
                pricing.amount_uses_key += 1
                pricing.save()
                messages.success(request, 'Coupon used successfully.')
                return redirect(member)
            if 'coupon_value' in request.session:
                currency = 'eth'
                value = pricing.get_crypto_value(currency='ETH')
            elif 'coupon_value_btc' in request.session:
                currency = 'btc'
                value = pricing.get_crypto_value(currency='BTC')
        except ObjectDoesNotExist as odnExc:
            messages.error(request, 'Coupon not found!')
            return redirect(member)
    elif 'payment_value_eth' in request.session:
        value = request.session.get('payment_value_eth')
        currency = 'eth'
        try:
            pricing = Pricing_Fiat.objects.get(id=value, only_available_using_key=False, is_free=False)
            value = pricing.get_crypto_value(currency='ETH')

        except ObjectDoesNotExist as odnExc:
            messages.error(request, 'Requested Payment Value could not validate!')
            return redirect(member)
    elif 'payment_value_btc' in request.session:
        currency = 'btc'
        value = request.session.get('payment_value_btc')
        try:
            pricing = Pricing_Fiat.objects.get(id=value, only_available_using_key=False, is_free=False)
            value = pricing.get_crypto_value(currency='BTC')

        except ObjectDoesNotExist as odnExc:
            messages.error(request, 'Requested Payment Value could not validate!')
            return redirect(member)

    # Value is checked by the finalization function in receivers.py
    form = PaymentForm_Crypto({
        'coin': currency,
        'value': value,
        'browser_request': request
    })
    if form.is_valid():
        payment = form.save(commit=False)
        payment.user = request.user
        payment.pricing = pricing
        payment.save()
    else:
        raise Exception("THIS SHOULDN'T HAPPEN")
    invoice = cryptapi_invoice(
        request=request,
        order_id=payment.auto_increment_id,
        coin=payment.coin,
        value=payment.value
    )
    payment_address = invoice.address()
    if payment_address is not None:
        # Show payment to the user
        response = render(
            request,
            'user_area/user/payment.html',
            {
                'status': 'Awaiting Order...',
                'currency': invoice.coin,
                'price': invoice.value,
                'receiveAddress': payment_address,
                'orderId': payment.auto_increment_id,
                'memberPage': True
            }
        )
        print("################################Payment Request##############################")
        print("User: " + request.user.__str__() + " has requested a new payment")
        print("Request ID: " + str(payment.pk) + " | to: " + payment_address + " | value: " + str(value))
        print("#############################################################################")
        response.set_cookie('payment_session', payment.auto_increment_id)
        if not 'order_id' in request.GET:
            return HttpResponseRedirect('/member/account/payment?order_id=' + str(payment.auto_increment_id))
        return response
    else:
        print(
            "AN PAYMENT CREATION ERROR HAS OCCURED PLEASE READ RequestLogs ON ADMIN AND TRY AGAIN IF IT STILL DOESN'T WORK CONTACT YOUR DEVELOPER!!")
    return render(request, 'user_area/user/payment.html',
                  {'status': 'Error', 'currency': "", 'price': "Please contact support or try again"})


@staff_member_required
def test_order_view(request):
    from .models import Payment_Crypto
    Payments = Payment_Crypto.objects.all()
    order_id = Payments[len(Payments) - 1].auto_increment_id
    value = 1000000000000000
    from cryptapi.models import Payment
    Payments = Payment.objects.all()
    payment = Payments[len(Payments) - 1]
    from .receivers import PaymentCryptoReceiver
    PaymentCryptoReceiver.payment_received(order_id, payment, value)
    messages.success(request,
                     "Done?\nRemember That this function works with the last object in the Payment Object List\nThis may cause bugs!")
    return redirect(member)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@staff_member_required
def export_trial_users_as_csv(request):
    if not (request.user.userLevel == 4):
        messages.error(request,
                       "You are not authorized to do this!\nRequires being Staff and Administration Status!")
        return redirect(member)
    """A view that streams a large CSV file."""
    users = get_user_model().objects.all()
    rows = ([str(i), users[i].username, users[i].email, users[i].sub_since, users[i].sub_until] for i in
            range(len(users)) if users[i].userLevel == 1)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Provisn_Trial_Users(' + timezone.now().strftime(
        "%Y-%m-%d - %H-%M-%S") + ').csv"'
    return response


@staff_member_required
def export_subscribed_users_as_csv(request):
    if not (request.user.userLevel == 4):
        messages.error(request,
                       "You are not authorized to do this!\nRequires being Staff and Administration Status!")
        return redirect(member)
    users = get_user_model().objects.all()
    rows = ([str(i), users[i].username, users[i].email, users[i].sub_since, users[i].sub_until] for i in
            range(len(users)) if users[i].userLevel == 2)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Provisn_Sub_Users(' + timezone.now().strftime(
        "%Y-%m-%d - %H-%M-%S") + ').csv"'
    return response


@staff_member_required
def export_subscribed_and_trial_users_as_csv(request):
    if not (request.user.userLevel == 4):
        messages.error(request,
                       "You are not authorized to do this!\nRequires being Staff and Administration Status!")
        return redirect(member)
    users = get_user_model().objects.all()
    rows = ([str(i), users[i].username, users[i].email, users[i].sub_since, users[i].sub_until] for i in
            range(len(users)) if (users[i].userLevel == 2 or users[i].userLevel == 1))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Provisn_Sub_And_Trial_Users(' + timezone.now().strftime(
        "%Y-%m-%d - %H-%M-%S") + ').csv"'
    return response


@staff_member_required
def export_all_users_as_csv(request):
    if not (request.user.userLevel == 4):
        messages.error(request,
                       "You are not authorized to do this!\nRequires being Staff and Administration Status!")
        return redirect(member)
    users = get_user_model().objects.all()
    rows = ([str(i), users[i].username, users[i].email, str(users[i].userLevel), users[i].sub_since, users[i].sub_until]
            for i in range(len(users)))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Provisn_Users(' + timezone.now().strftime(
        "%Y-%m-%d - %H-%M-%S") + ').csv"'
    return response


@staff_member_required
def staff_prolong_subscription(request):
    from userdashboard.accounts import UserMethods
    UserMethods.prolongUserSubscriptionByRequest(request)
    messages.success(request, "Successfully extended subscription!")
    return redirect(member)


def BugReporter(request):
    Title = "Bug Reporter"
    subHeader = "Report bugs or website improvements here"
    if request.method == "POST":
        form = BugReportForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Form sent successfully.\nThanks, we'll  contact if we have questions.")
            return redirect('member')
    else:
        form = BugReportForm
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader})
        return response
    return render(request, 'user_area/user/BugReporter.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@staff_member_required
def EditBeams(request):
    ...


@login_required()
def DetailsBeams(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Beam, pk=pk)

    navId = 'beamsNavLink'
    PageRefAddContent = 'NewBeams'

    response = render(request, 'user_area/user/Content_Pages/Beam.html',
                      {'post': post, 'navId': navId, 'PageRefAddContent': PageRefAddContent})
    return response


@staff_member_required
def NewBeams(request):
    Title = "Create new Beams Post"
    subHeader = "Use your given power as a staff member to create impressive new content"
    if request.method == 'POST':
        form = BeamsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user
            post.save()
            return redirect('DetailsBeams', pk=post.pk)
    else:
        form = BeamsForm()
    return render(request, 'user_area/user/ContentCreation.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@staff_member_required()
def PublishBeams(request, pk):
    post = get_object_or_404(Beam, pk=pk)
    post.publish()
    return redirect(DetailsBeams, pk=pk)


@staff_member_required
def DraftsBeams(request):
    beams = Beam.objects.exclude(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(beams, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    beams = paginator.get_page(page)
    Title = "Beams Drafts"
    subHeader = "Robust, dependable, and comprehensive signal calls"
    PageRefAddContent = 'NewBeams'

    response = render(request, 'user_area/user/Content_Pages/Beams.html',
                      {'items': beams, 'pagetitle': Title, 'navId': 'beamsNavLink', 'subHeader': subHeader,
                       'PageRefAddContent': PageRefAddContent, 'is_draft': True})
    return response


@login_required
def AddCommentToBeam(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Beam, pk=pk)
    if request.method == "POST":
        form = BeamCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('DetailsBeams', pk=post.pk)
    else:
        form = BeamCommentForm()
        Title = "Add Beams Comment"
        postTitle = get_object_or_404(Beam, pk=pk).title
        subHeader = 'Post:' + postTitle
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader, })
    return response


@staff_member_required
def EditEvents(request):
    ...


@login_required
def AddCommentToEvent(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(BlockchainEvent, pk=pk)
    if request.method == "POST":
        form = BlockchainEventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('DetailsEvents', pk=post.pk)
    else:
        form = BlockchainEventCommentForm()
        Title = "Add Event Comment"
        subHeader = ""
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader, })
    return response


def PublishEvents(request, pk):
    post = get_object_or_404(BlockchainEvent, pk=pk)
    post.publish()
    return redirect(DetailsBeams, pk=pk)


@staff_member_required
def DraftsEvents(request):
    events = BlockchainEvent.objects.exclude(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(events, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    Title = "Beams"

    response = render(request, 'user_area/user/ContentListPage.html',
                      {'items': events, 'pagetitle': Title})
    return response


@login_required
def DetailsEvents(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(BlockchainEvent, pk=pk)
    PageRefAddContent = 'NewBlockchainEvents'

    response = render(request, 'user_area/user/Content_Pages/Calendar-Entry.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response


@staff_member_required
def NewEvents(request):
    Title = "Create new Blockchain Event Post"
    subHeader = "Use your given power as a staff member to create impressive new content"
    if request.method == 'POST':
        form = BlockchainEventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(DetailsEvents, pk=post.pk)
    else:
        form = BlockchainEventForm()
    return render(request, 'user_area/user/ContentCreation.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@staff_member_required()
def EditBN(request):
    ...


def PublishBN(request, pk):
    post = get_object_or_404(BlockchainNew, pk=pk)
    post.publish()
    return redirect(DetailsBN, pk=pk)


@login_required
def DetailsBN(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(BlockchainNew, pk=pk)
    navId = 'newsNavLink'
    PageRefAddContent = 'NewBlockchainNews'

    response = render(request, 'user_area/user/Content_Pages/News-Article.html',
                      {'post': post, 'navId': navId,
                       'PageRefAddContent': PageRefAddContent})
    return response


@staff_member_required
def DraftsBN(request):
    news = BlockchainNew.objects.exclude(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(news, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    Title = "News Drafts"

    response = render(request, 'user_area/user/Content_Pages/News.html',
                      {'items': news, 'pagetitle': Title, 'is_draft': True})
    return response


@login_required
def AddCommentToBN(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(BlockchainNew, pk=pk)
    if request.method == "POST":
        form = BlockchainNewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('DetailsNews', pk=post.pk)
    else:
        form = BlockchainNewsCommentForm()
        Title = "Add News Comment"
        subHeader = ""
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader, })
    return response


@staff_member_required
def NewBN(request):
    Title = "Create new News Post"
    subHeader = "Use your given power as a staff member to create impressive new content"
    if request.method == 'POST':
        form = BlockchainNewsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('DetailsNews', pk=post.pk)
    else:
        form = BlockchainNewsForm()
    return render(request, 'user_area/user/ContentCreation.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@staff_member_required
def EditAIEntry(request):
    ...


@login_required
def DetailsAIEntry(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(ArtificialIntelligence, pk=pk)
    navId = 'aiNavLink'
    PageRefAddContent = 'NewAI'

    percentageValuePosition = post.get_percentage_value_position() + 15
    percentageValue = post.text[percentageValuePosition:percentageValuePosition + 5].replace('%', '').replace('<',
                                                                                                              '').replace(
        '>', '')
    if 'ng' in percentageValue:
        percentageValue = post.text[percentageValuePosition + 4:percentageValuePosition + 9].replace('%', '').replace(
            '<', '').replace('>', '')
    percentageValueNumber = float(percentageValue)
    percentageValueInDeg = 180 / 100 * float(percentageValue)

    GaugeClass = ''
    if percentageValueNumber > 65:
        GaugeClass = 'gradient-hot'
    elif percentageValue:
        GaugeClass = 'gradient-cold'

    response = render(request, 'user_area/user/Content_Pages/AI-Article.html',
                      {
                          'post': post,
                          'navId': navId,
                          'PageRefAddContent': PageRefAddContent,
                          'GaugeDegree': percentageValueInDeg,
                          'GaugePercent': percentageValue,
                          'GaugeClass': GaugeClass,
                      })
    return response


def PublishAI(request, pk):
    post = get_object_or_404(ArtificialIntelligence, pk=pk)
    post.publish()
    return redirect(DetailsAIEntry, pk=pk)


@staff_member_required
def DraftsAI(request):
    ai = Beam.objects.exclude(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(ai, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    beams = paginator.get_page(page)
    Title = "A.I. Drafts"

    response = render(request, 'user_area/user/Content_Pages/AI.html',
                      {'items': beams, 'pagetitle': Title})
    return response


@login_required
def AddCommentToAIEntry(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(ArtificialIntelligence, pk=pk)
    if request.method == "POST":
        form = AICommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('DetailsAI', pk=post.pk)
    else:
        form = AICommentForm()
        Title = "Add AI Comment"
        subHeader = ""
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader, })
    return response


@staff_member_required
def NewAIEntry(request):
    Title = "Create new AI Post"
    subHeader = "Use your given power as a staff member to create impressive new content"
    if request.method == 'POST':
        form = ArtificialIntelligenceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('DetailsAI', pk=post.pk)
    else:
        form = ArtificialIntelligenceForm()
    return render(request, 'user_area/user/ContentCreation.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@staff_member_required
def EditTA(request):
    ...


@login_required()
def DetailsTA(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(TechnicalAnalysi, pk=pk)
    navId = 'technicalAnalysisNavLink'
    PageRefAddContent = 'NewTA'

    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post, 'navId': navId,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required()
def DetailsTA_f(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_Faibik, pk=pk)
    navId = 'technicalAnalysisNavLink'
    PageRefAddContent = 'NewTA'

    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post, 'navId': navId,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required()
def DetailsTA_ka(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_KhaledAbdulaziz, pk=pk)
    navId = 'technicalAnalysisNavLink'
    PageRefAddContent = 'NewTA'

    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post, 'navId': navId,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required()
def DetailsTA_am(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_alanmasters, pk=pk)
    navId = 'technicalAnalysisNavLink'
    PageRefAddContent = 'NewTA'

    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post, 'navId': navId,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required()
def DetailsTA_cn(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(Content_CryptoNTez, pk=pk)
    navId = 'technicalAnalysisNavLink'
    PageRefAddContent = 'NewTA'

    response = render(request, 'user_area/user/Content_Pages/TA-Article.html',
                      {'post': post, 'navId': navId,
                       'PageRefAddContent': PageRefAddContent})
    return response


@staff_member_required
def PublishTA(request, pk):
    post = get_object_or_404(TechnicalAnalysi, pk=pk)
    post.publish()
    return redirect(DetailsTA, pk=pk)


@staff_member_required
def DraftsTA(request):
    ta = TechnicalAnalysi.objects.exclude(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(ta, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    ta = paginator.get_page(page)
    Title = "Technical Analysis Drafts"

    response = render(request, 'user_area/user/Content_Pages/Technical-Analysis.html',
                      {'items': ta, 'pagetitle': Title, 'is_draft': True})
    return response


@login_required
def AddCommentToTA(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(TechnicalAnalysi, pk=pk)
    if request.method == "POST":
        form = TACommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('DetailsTA', pk=post.pk)
    else:
        form = TACommentForm()
        Title = "Add Technical analysis Comment"
        subHeader = ""
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader, })
    return response


@staff_member_required
def NewTA(request):
    Title = "Create new Technical Analysis Post"
    subHeader = "Use your given power as a staff member to create impressive new content"
    if request.method == 'POST':
        form = TechnicalAnalysisForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('DetailsTA', pk=post.pk)
    else:
        form = TechnicalAnalysisForm()
    return render(request, 'user_area/user/ContentCreation.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@staff_member_required
def EditTW(request):
    ...


def PublishTW(request, pk):
    post = get_object_or_404(TokenWatchlist, pk=pk)
    post.publish()
    return redirect(DetailsTW, pk=pk)


@staff_member_required
def DraftsTW(request):
    tw = TokenWatchlist.objects.exclude(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(tw, AMOUNT_CONTENT_PAGE_OBJECTS_PER_PAGE)
    page = request.GET.get('page')
    tw = paginator.get_page(page)
    Title = "Token Spotlight Drafts"

    response = render(request,
                      'user_area/user/Content_Pages/Token-Watchlist.html',
                      {'items': tw, 'pagetitle': Title})
    return response


@login_required
def DetailsTW(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(TokenWatchlist, pk=pk)
    PageRefAddContent = 'NewTW'

    response = render(request, 'user_area/user/Content_Pages/TW-Article.html',
                      {'post': post,
                       'PageRefAddContent': PageRefAddContent})
    return response


@login_required
def AddCommentToTW(request, pk):
    if not (isUserSubscribedByRequest(request)):
        printUserSubscriptionHasRunOut(request)
        return redirect(member)
    post = get_object_or_404(TokenWatchlist, pk=pk)
    if request.method == "POST":
        form = TWCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('DetailsTW', pk=post.pk)
    else:
        form = TWCommentForm()
        Title = "Add Token Watchlist Comment"
        subHeader = ""
        response = render(request, 'user_area/user/ContentCreation.html',
                          {'form': form, 'pagetitle': Title, 'subHeader': subHeader})
    return response


@staff_member_required
def NewTW(request):
    Title = "Create new Token Watchlist Post"
    subHeader = "Use your given power as a staff member to create impressive new content"
    if request.method == 'POST':
        form = TokenWatchlistForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.coin_icon = form.cleaned_data['coin_icon']
            post.save()
            return redirect('DetailsTW', pk=post.pk)
    else:
        form = TokenWatchlistForm()
    return render(request, 'user_area/user/ContentCreation.html',
                  {'form': form, 'pagetitle': Title, 'subHeader': subHeader})


@login_required
def FriendInvitationOverview(request):
    page_title = 'Invite Friends'
    time_left = None
    if request.user.sub_until > timezone.now():
        time_left = request.user.sub_until - timezone.now()
        time_left = time_left.days
    from referral.utils import getUserReferralToken
    ref_token = getUserReferralToken(request.user)
    from referral.models import Referral, SignedUpUserReferral
    from django.forms.models import model_to_dict
    refobject = Referral.objects.get(User=request.user)

    if request.POST:
        from referral.forms import OpenPayoutForm
        form = OpenPayoutForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.reftoken = refobject
            from django.db import IntegrityError
            try:
                post.save()
            except IntegrityError:
                messages.error(request, 'Payout has already been requested! Please wait for your payout.')
                return redirect(member)
            return redirect(payout)

    signed_up_users = SignedUpUserReferral.objects.filter(RefToken=refobject)
    user_list = []
    i = 0
    for user in signed_up_users:
        user_list.append(model_to_dict(user))
        user_list[i]['email'] = user.User.email
        user_list[i]['date_joined'] = user.User.date_joined
        if refobject.ReferralSubscribers.filter(email=user.User.email).exists():
            user_list[i]['has_subscribed'] = 'Yes'
        else:
            user_list[i]['has_subscribed'] = 'No'
        if user_list[i]['has_subscribed'] == 'Yes':
            user_list[i]['free_time_earned'] = '<span style="color:green;">+10 USD</span>'
        else:
            user_list[i]['free_time_earned'] = 0
        i += 1
        print()
    payout_form = None
    if refobject.Amount_open_payoff >= 20:
        from referral.forms import OpenPayoutForm
        payout_form = OpenPayoutForm()
    return render(request, 'user_area/user/InviteOverview.html', {
        'pagetitle': page_title,
        'ref_token': ref_token,
        'time_left': time_left,
        'referral_list': user_list,
        'refobject': refobject,
        'payout_form': payout_form
    })


@staff_member_required
def referral_pay_off_list(request):
    from referral.models import Referral, OpenPayout
    if request.POST:
        paid_off_user_email = request.POST['pay-out']
        paid_off_user = CustomUser.objects.get(email=paid_off_user_email)
        payout = OpenPayout.objects.get(user=paid_off_user)
        payout.delete()
        referral = Referral.objects.get(User=paid_off_user)
        referral.To_be_paid_off = False
        referral.Amount_paid_off = referral.Amount_open_payoff
        referral.Amount_open_payoff = 0
        referral.save()
        print('paying off {}'.format(paid_off_user))
    page_title = 'Referral Users to pay off'
    users = Referral.objects.filter(To_be_paid_off=True)
    data = []

    i = 0
    for user in users:
        payout = OpenPayout.objects.get(user=user.User)
        data.append({
            'reftoken': user,
            'user': user.User,
            'Amount_open_payoff': user.Amount_open_payoff,
            'payout': payout
        })
    return render(request, 'user_area/user/OpenPayoffs.html', {'pay_off_users': data, 'pagetitle': page_title})


@login_required
def payout(request):
    from referral.models import Referral
    user = request.user
    referral = Referral.objects.get(User=user)
    if referral.Amount_open_payoff >= 20:
        referral.To_be_paid_off = True
        referral.save()
        messages.success(request, 'Your open referral reward has been marked to be paid out! Thanks for using Provisn')
    else:
        messages.error(request, 'You need an open payoff of at least 20$!')
    return redirect(member)

@login_required
def cancel_subscription(request):
    sub = get_object_or_404(ActiveSubscription, user=request.user)
    stripe.Subscription.delete(sub.subscription.subscription_id)
    sub.delete()
    response = render(request, 'user_area/user/payment_pages/sub_cancelled.html', {})
    return response

@staff_member_required
def test_user_notification(request):
    messages.success(request, "THIS IS A NOTIFICATION!")
    return redirect(member)


### REST API

from rest_framework.views import APIView
from rest_framework.response import Response as restResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from plutus.settings import CMC_API
from coinpaprika import client as CoinPaprika


class Preview_Links(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            import urllib.parse
            url = urllib.parse.quote(list(request.GET.items())[0][0], safe='')
        except Exception as ex:
            return restResponse()

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

        try:
            response = session.get(get_url, params=parameters)
            data = json.loads(response.text)
            return restResponse(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return restResponse()


class GetLatestListings(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if 'limit' in request.GET:
            limit = request.GET['limit']
        else:
            limit = 25

        client = CoinPaprika.Client()
        data = client.tickers(quotes='USD,BTC')
        return restResponse(data[:limit])


class GetAllCryptoCurrencies(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):

        client = CoinPaprika.Client()
        data = client.coins()

        try:
            if 'save_as_models' in request.GET and request.user.is_staff:
                for currency in data:
                    if DEBUG:
                        print(currency)
                    new_coin = Coin(
                        name=currency['name'],
                        symbol=currency['symbol'],
                        type=currency['type'],
                        coinpaprika_id=currency['id'],
                    )
                    from django.db.utils import IntegrityError
                    try:
                        new_coin.save()
                    except IntegrityError:
                        continue
            return restResponse(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return restResponse('Error')


class GetCryptoCurrencyPricePerformance(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            coin = None
            if 'id' in request.GET:
                if ',' in request.GET['id']:
                    coin_multiple = request.GET['id']
                else:
                    coin = Coin.objects.get(cmc_id=request.GET['id'])
            elif 'slug' in request.GET:
                coin = Coin.objects.get(slug=request.GET['slug'])
            elif 'symbol' in request.GET:
                coin = Coin.objects.get(symbol=request.GET['symbol'])
            else:
                return restResponse('No currency defined!')
        except Exception as ex:
            return restResponse()

        app_id = CMC_API
        get_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/price-performance-stats/latest'

        parameters = {
            'id': coin.cmc_id if coin else coin_multiple
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': app_id
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(get_url, params=parameters)
            data = json.loads(response.text)
            return restResponse(data['data'])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return restResponse()


class GetCryptoCurrencyInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        try:
            if 'id' in request.GET:
                coin = Coin.objects.get(cmc_id=request.GET['id'])
            elif 'slug' in request.GET:
                coin = Coin.objects.get(slug=request.GET['slug'])
            elif 'symbol' in request.GET:
                coin = Coin.objects.get(symbol=request.GET['symbol'])
            else:
                return restResponse('No currency defined!')
        except Exception as ex:
            return restResponse()

        app_id = CMC_API
        get_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

        parameters = {
            'id': coin.cmc_id
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': app_id
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(get_url, params=parameters)
            data = json.loads(response.text)
            return restResponse(data['data'][str(coin.cmc_id)])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return restResponse()


class GetCryptoCurrencyMarketQuotes(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        coin = None
        try:
            coin = Coin.objects.get(coinpaprika_id=request.GET['id'])
        except Exception as ex:
            return HttpResponse(status=400)
        client = CoinPaprika.Client()
        data = client.ticker(coin.coinpaprika_id)
        return restResponse(data)


class GetDashboardEvents(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = BlockchainEvent.objects.filter(
            date_of_event__year=timezone.now().year,
            date_of_event__month=timezone.now().month,
            published_date__lte=timezone.now()
        ).order_by('date_of_event').values()
        items = []

        for event in events:
            new_dict = {}
            new_dict['title'] = event['title']
            new_dict['text'] = event['text'][:150] + '...'
            new_dict['day'] = event['date_of_event'].day
            new_dict['date_of_event'] = event['date_of_event'].strftime('%b %d %Y')
            new_dict['location'] = event['location']
            new_dict['event_url'] = event['event_url']
            #if event['set_color']:
            new_dict['color_class'] = event['color_class']
            items.append(new_dict)
        return restResponse(items)


class GetPaymentStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not request.GET:
            return restResponse('Please enter order id')
        if 'order_id' in request.GET:
            id = request.GET.get('order_id')
        payment = cryptapi_request.objects.get(order_id=id)
        payment_info = {}
        payment_info['status'] = payment.status
        payment_info['address'] = payment.address_in
        try:
            payment_wrapper = Payment_Crypto.objects.get(user=request.user, auto_increment_id=id)
            payment_info['amount'] = payment_wrapper.value
            payment_info['received'] = payment_wrapper.payment_received
            payment_info['currency'] = payment_wrapper.coin
        except Exception:
            return restResponse('Not Authorized!')
        return restResponse(payment_info)


class TestCoinpaprika(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        client = CoinPaprika.Client()
        data = client.ticker("btc-bitcoin")
        return restResponse(data)


@csrf_exempt
def stripe_webhook(request):
    if DEBUG:
        print('Stripe Webhook Received!')
        print(request)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        if DEBUG:
            print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        if DEBUG:
            print(e)
        return HttpResponse(status=400)
    log = None
    try:
        log = StripeWebhook(data=json.dumps(event))
        log.save()
    except Exception:
        pass
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        from .accounts import UserMethods
        session = event['data']['object']

        # Fulfill the purchase...
        payment = Payment_Fiat.objects.get(session_id=event['data']['object']['id'])
        payment.payment_fulfilled = True
        payment.fulfilled_at = timezone.now()
        payment.save()
        try:
            pricing = payment.pricing
            pricing.amount_uses_usd = pricing.amount_uses_usd + 1
            pricing.save()
        except Exception:
            pass
        UserMethods.prolongUserSubscriptionByUserObject(
            payment.user,
            timezone.timedelta(payment.pricing.subscription_time_in_days)
        )

        ### Referral Handling
        try:
            from referral.models import SignedUpUserReferral
            refToken = SignedUpUserReferral.objects.get(User=payment.user).RefToken
            if not refToken.ReferralSubscribers.filter(email=payment.user.email).exists():
                refToken.AmountReferrals += 1
                refToken.check_reward()
                refToken.ReferralSubscribers.add(payment.user)
                refToken.save()
            else:
                error_msg = 'User referral has already been gifted'
                print(error_msg)
        except SignedUpUserReferral.DoesNotExist:
            pass
        except Exception:
            pass

        if DEBUG:
            print('Successfully Finished Credit Card Payment ' + session['id'])

    elif event['type'] == 'invoice.upcoming':
        if DEBUG:
            print('Invoice Incoming')
            print(event)
        session = event['data']['object']
        user = CustomUser.objects.get(email=session['customer_email'])
        invoice = ud_models.Invoice(
            user=user,
            status=session['status'],
            amount_due=session['amount_due'],
            amount_paid=session['amount_paid'],
            amount_remaining=session['amount_remaining'],
            billing_type=session['billing'],
            billing_reason=session['billing_reason'],
            currency=session['currency'],
            account_country=session['account_country'],
            invoice_id=session['id'],
            invoice_url=session['hosted_invoice_url'],
            invoice_pdf=session['invoice_pdf'],
            payment_plan=session['lines']['data'][0]['plan']['id'],
            payment_intent=session['payment_intent'],
            payment_number=session['number'],
            subscription_id=session['subscription'],
            data=log,
        )
        invoice.save()
        if DEBUG:
            print(invoice.billing_reason)


    elif event['type'] == 'invoice.payment_succeeded':
        from .accounts import UserMethods
        if DEBUG:
            print('Invoice succeeded')
            print(str(event))
        session = event['data']['object']
        print(vars(event))
        user = CustomUser.objects.get(email=session['customer_email'])
        invoice = None
        try:
            invoice = ud_models.Invoice.objects.get(payment_number=session['number'], user=user)
            invoice.user = user
            invoice.status = session['status']
            invoice.amount_due = session['amount_due']
            invoice.amount_paid = session['amount_paid']
            invoice.amount_remaining = session['amount_remaining']
            invoice.billing_type = session['billing']
            invoice.billing_reason = session['billing_reason']
            invoice.currency = session['currency']
            invoice.account_country = session['account_country']
            invoice.invoice_id = session['id']
            invoice.invoice_url = session['hosted_invoice_url']
            invoice.invoice_pdf = session['invoice_pdf']
            invoice.payment_plan = session['lines']['data'][0]['plan']['id']
            invoice.payment_intent = session['payment_intent']
            invoice.payment_number = session['number']
            invoice.subscription_id = session['subscription']
            invoice.updated = timezone.now()
            invoice.data = log
        except ObjectDoesNotExist:
            invoice = ud_models.Invoice(
                user=user,
                status=session['status'],
                amount_due=session['amount_due'],
                amount_paid=session['amount_paid'],
                amount_remaining=session['amount_remaining'],
                billing_type=session['billing'],
                billing_reason=session['billing_reason'],
                currency=session['currency'],
                account_country=session['account_country'],
                invoice_id=session['id'],
                invoice_url=session['hosted_invoice_url'],
                invoice_pdf=session['invoice_pdf'],
                payment_plan=session['lines']['data'][0]['plan']['id'],
                payment_intent=session['payment_intent'],
                payment_number=session['number'],
                subscription_id=session['subscription'],
                data=log,
            )
        if invoice is not None:
            invoice.save()
            if invoice.billing_reason == 'subscription_create':
                sub = ActiveSubscription(
                    user=user,
                    subscription=invoice
                )
                sub.save()
                print('sub saved')
        if DEBUG:
            print('Successfully Finished Automatic Recurring Credit Card Payment ' + session['id'])

    elif event['type'] == 'invoice.payment_action_required':
        if DEBUG:
            print('Invoice Payment Action required')
            print(event)
        session = event['data']['object']
        print(vars(event))
        user = CustomUser.objects.get(email=session['customer_email'])
        invoice = None
        try:
            invoice = ud_models.Invoice.objects.get(payment_number=session['number'], user=user)
            invoice.user = user
            invoice.status = session['status']
            invoice.amount_due = session['amount_due']
            invoice.amount_paid = session['amount_paid']
            invoice.amount_remaining = session['amount_remaining']
            invoice.billing_type = session['billing']
            invoice.billing_reason = session['billing_reason']
            invoice.currency = session['currency']
            invoice.account_country = session['account_country']
            invoice.invoice_id = session['id']
            invoice.invoice_url = session['hosted_invoice_url']
            invoice.invoice_pdf = session['invoice_pdf']
            invoice.payment_plan = session['lines']['data'][0]['plan']['id']
            invoice.payment_intent = session['payment_intent']
            invoice.payment_number = session['number']
            invoice.subscription_id = session['subscription']
            invoice.updated = timezone.now()
            invoice.data = log
        except ObjectDoesNotExist:
            invoice = ud_models.Invoice(
                user=user,
                status=session['status'],
                amount_due=session['amount_due'],
                amount_paid=session['amount_paid'],
                amount_remaining=session['amount_remaining'],
                billing_type=session['billing'],
                billing_reason=session['billing_reason'],
                currency=session['currency'],
                account_country=session['account_country'],
                invoice_id=session['id'],
                invoice_url=session['hosted_invoice_url'],
                invoice_pdf=session['invoice_pdf'],
                payment_plan=session['lines']['data'][0]['plan']['id'],
                payment_intent=session['payment_intent'],
                payment_number=session['number'],
                subscription_id=session['subscription'],
                data=log,
            )
        if invoice is not None:
            invoice.save()

    return HttpResponse(status=200)
