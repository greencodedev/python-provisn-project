from django.urls import path, include
from . import views
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

# Well this explains itself i think
# path(uri, view method, name (e.g. grabbing urls));
# app_name = 'userdashboard'

urlpatterns = [
    url(r'^', include('TelegramHandler.urls', namespace='TelegramHandler')),
    url(r'^', include('ContentScraper.urls', namespace='ContentScraper')),

    path('', views.userDashboard, name="user_area"),
    path('beams/', views.userBeams, name='user_beams'),
    path('events/', views.userBlockchainEvents, name='user_events'),
    path('news/', views.userNews, name="user_news"),
    path('ai/', views.userAI, name='user_ai'),
    path('technical_analysis/', views.userTechnicalAnalysis, name='user_technical_analysis'),
    path('token_spotlight/', views.userTokenWatchlist, name='user_token_watchlist'),

    path('invite/', views.FriendInvitationOverview, name='FriendInvitationOverview'),

    url(r'^search/$', views.search, name='search'),

    path('account/payment/', views.order_creation_view, name='order_creation_view'),
    path('account/paymentc', views.credit_card_payment_charge, name='credit_card_payment_charge'),
    path('account/paymentc/success', views.credit_card_payment_charge_successful, name='credit_card_payment_charge_successful'),
    path('account/paymentc/cancelled', views.credit_card_payment_charge_cancelled, name='credit_card_payment_charge_cancelled'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('logout/', views.logOut, name='logout'),
    path('account/', views.member, name='member'),
    path('account/payout', views.payout, name='payout'),
    path('account/cancel_subscription', views.cancel_subscription, name='cancel_user_subscription'),
    path('staff/', views.userAdminTools, name='user_admin_tools'),
    path('settings/', views.userSettings, name='user_settings'),
    path('changelog/', views.userChangelog, name='user_changelog'),

    path('invite_friends/', views.send_friend_invitation, name='friend_inviter'),

    path('export/csv/trial_users', views.export_trial_users_as_csv, name='export_users_trial'),
    path('export/csv/subscribed_users', views.export_subscribed_users_as_csv, name='export_users_subscribed'),
    path('export/csv/all', views.export_all_users_as_csv, name='export_users_all'),
    path('export/csv/sub_and_trial_users', views.export_subscribed_and_trial_users_as_csv, name='export_users_sub_and_trial'),

    path('staff/extend_subscription', views.staff_prolong_subscription, name='staff_extend_subscription'),
    path('staff/test_payment_successful', views.test_order_view, name='staff_test_payment_successful'),

    path('bugreporter', views.BugReporter, name='BugReporter'),

    path('beams/<int:pk>/', views.DetailsBeams, name='DetailsBeams'),
    path('events/<int:pk>/', views.DetailsEvents, name='DetailsEvents'),
    path('news/<int:pk>/', views.DetailsBN, name='DetailsNews'),
    path('ai/<int:pk>/', views.DetailsAIEntry, name='DetailsAI'),
    path('technical_analysis/<int:pk>/', views.DetailsTA, name='DetailsTA'),
    path('technical_analysis_cn/<int:pk>/', views.DetailsTA_cn, name='DetailsTA_m'),
    path('technical_analysis_f/<int:pk>/', views.DetailsTA_f, name='DetailsTA_f'),
    path('technical_analysis_ka/<int:pk>/', views.DetailsTA_ka, name='DetailsTA_ka'),
    path('technical_analysis_am/<int:pk>/', views.DetailsTA_am, name='DetailsTA_am'),
    path('token_spotlight/<int:pk>/', views.DetailsTW, name='DetailsTW'),

    path('beams/new/', views.NewBeams, name='NewBeams'),
    path('events/new/', views.NewEvents, name='NewEvents'),
    path('news/new/', views.NewBN, name='NewBN'),
    path('ai/new/', views.NewAIEntry, name='NewAIEntry'),
    path('technical_analysis/new/', views.NewTA, name='NewTA'),
    path('token_spotlight/new/', views.NewTW, name='NewTW'),

    url(r'^beams/(?P<pk>\d+)/publish/$', views.PublishBeams, name='PublishBeams'),
    url(r'^events/(?P<pk>\d+)/publish/$', views.PublishEvents, name='PublishEvents'),
    url(r'^news/(?P<pk>\d+)/publish/$', views.PublishBN, name='PublishNews'),
    url(r'^ai/(?P<pk>\d+)/publish/$', views.PublishAI, name='PublishAI'),
    url(r'^technical_analysis/(?P<pk>\d+)/publish/$', views.PublishTA, name='PublishTA'),
    url(r'^token_spotlight/(?P<pk>\d+)/publish/$', views.PublishTW, name='PublishTW'),

    path('beams/drafts/', views.DraftsBeams, name='DraftsBeams'),
    path('events/drafts/', views.DraftsEvents, name='DraftsEvents'),
    path('news/drafts/', views.DraftsBN, name='DraftsBN'),
    path('ai/drafts/', views.DraftsAI, name='DraftsAIEntry'),
    path('technical_analysis/drafts/', views.DraftsTA, name='DraftsTA'),
    path('token_spotlight/drafts/', views.DraftsTW, name='DraftsTW'),

    url(r'^beams/(?P<pk>\d+)/comment/$', views.AddCommentToBeam, name='AddCommentBeams'),
    url(r'^events/(?P<pk>\d+)/comment/$', views.AddCommentToEvent, name='AddCommentEvent'),
    url(r'^news/(?P<pk>\d+)/comment/$', views.AddCommentToBN, name='AddCommentNews'),
    url(r'^ai/(?P<pk>\d+)/comment/$', views.AddCommentToAIEntry, name='AddCommentAI'),
    url(r'^technical_analysis/(?P<pk>\d+)/comment/$', views.AddCommentToTA, name='AddCommentTA'),
    url(r'^token_spotlight/(?P<pk>\d+)/comment/$', views.AddCommentToTW, name='AddCommentTW'),

    #url(r'^member/beams/(?P<pk>\d+)/remove/$', ..., name='RemoveBeams'),
    #url(r'^member/beams/(?P<pk>\d+)/comment')

    #url(r'^/messenger', views.MessagesOverview, name='messenger_overview')

    path('referral/pay_offs', views.referral_pay_off_list, name='ReferralPayOffs'),

    path('test_confirmed_page', views.test_activated_page, name='test_confirmed_page'),
    path('test_user_notification', views.test_user_notification, name='test_user_notification'),

    ### REST API
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('api/link_preview', views.Preview_Links.as_view(), name='link_preview'),
    path('api/get_all_crypto_currencies', views.GetAllCryptoCurrencies.as_view(), name='get_all_crypto_currencies'),
    path('api/get_crypto_currency_price_performance', views.GetCryptoCurrencyPricePerformance.as_view(), name='get_crypto_currency_price_performance'),
    path('api/get_crypto_currency_info', views.GetCryptoCurrencyInfo.as_view(), name='get_crypto_currency_info'),
    path('api/get_crypto_currency_market_quotes', views.GetCryptoCurrencyMarketQuotes.as_view(), name='get_crypto_currency_market_quotes'),
    path('api/dashboard_events', views.GetDashboardEvents.as_view(), name='dashboard_events'),
    path('api/payment_status', views.GetPaymentStatus.as_view(), name='payment_status'),
    path('api/latest_listings', views.GetLatestListings.as_view(), name='latest_listings'),
    path('api/test-coinpaprika', views.TestCoinpaprika.as_view(), name='test-coinpaprika'),
    # Stripe Webhook
    path('api/sw', views.stripe_webhook, name='sw'),

]