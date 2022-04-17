from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('rest/v1/calendar/init/', views.GoogleCalendarInitView,name='redirect'),
        path('rest/v1/calendar/redirect/', views.ConvinCalender.as_view()),
]