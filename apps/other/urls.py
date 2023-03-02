from django.urls import path, re_path, include

from other.views import StatisticsView


urlpatterns = [
    path('statistics', StatisticsView.as_view()),
]
