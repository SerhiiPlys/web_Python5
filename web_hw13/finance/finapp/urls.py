from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('record/', views.add_record, name='record'),
    path('report/', views.see_report, name='report'),
]