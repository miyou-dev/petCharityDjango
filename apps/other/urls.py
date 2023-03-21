from django.urls import path

from other.views.user_statistics_view import UserStatisticsView
from other.views.donate_amount_statistics_view import DonateAmountStatisticsView, DonateAmountTop, UserStatistics

urlpatterns = [
    path('', UserStatisticsView.as_view()),
    path('admin/donateAmountStatistics/', DonateAmountStatisticsView.as_view()),
    path('admin/donateAmountTop/', DonateAmountTop.as_view({'get': 'list'})),
    path('admin/userStatistics/', UserStatistics.as_view()),
]
