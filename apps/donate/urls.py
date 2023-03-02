from django.urls import path, re_path

from donate.views.donate_view import DonateView
from donate.views.donate_information_view import DonateInformationView
from donate.views.donation_list_information_view import DonationListInformationView
from donate.views.donation_list_view import DonationListView

#
urlpatterns = [

    # --------------------------------------------------宠物帮助众筹宠物--------------------------------------------------
    # 增 删 改
    path('create', DonateView.as_view({'post': 'create'})),
    path('update/<int:pk>', DonateView.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>', DonateView.as_view({'delete': 'destroy'})),

    # 查询
    path('get/<int:pk>', DonateInformationView.as_view({'get': 'retrieve'})),
    path('list', DonateInformationView.as_view({'get': 'list'})),

    # --------------------------------------------------宠物帮助众筹宠物捐赠名单--------------------------------------------------
    # 捐赠
    path('donate/userDonate', DonationListView.as_view({'post': 'create'})),
    path('donate/<int:pk>', DonationListInformationView.as_view({'get': 'retrieve'})),
    path('donate/list', DonationListInformationView.as_view({'get': 'list'})),

]
