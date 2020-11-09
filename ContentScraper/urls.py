from django.urls import path

from ContentScraper import views


app_name = 'ContentScraper'

urlpatterns = [
    path('technical_analysis_my/<int:pk>/', views.DetailsMoiseievYurii, name='DetailsMoiseievYurii'),
    path('technical_analysis_ka/<int:pk>/', views.DetailsKhaledAbdulaziz, name='DetailsKhaledAbdulaziz'),
    path('technical_analysis_f/<int:pk>/', views.DetailsFaibik, name='DetailsFaibik'),
    path('technical_analysis_hm/<int:pk>/', views.DetailsHamadaMark, name='DetailsHamadaMark'),
    path('technical_analysis_as/<int:pk>/', views.DetailsArShevelev, name='DetailsArShevelev'),
]