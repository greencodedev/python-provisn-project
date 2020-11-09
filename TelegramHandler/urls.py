from django.urls import path

from TelegramHandler import views


app_name = 'TelegramHandler'

urlpatterns = [
    path('news_cd/<int:pk>/', views.DetailsCoinDesk, name='DetailsCoinDesk'),
]