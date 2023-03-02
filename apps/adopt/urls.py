from django.urls import path

from adopt.views.pet_adopt_information_view import PetAdoptInformationView
from adopt.views.pet_adopt_view import PetAdoptView

# 宠物领养
urlpatterns = [

    # --------------------------------------------------宠物领养--------------------------------------------------
    # 增 删 改
    path('create', PetAdoptView.as_view({'post': 'create'})),
    path('update/<int:pk>', PetAdoptView.as_view({'patch': 'partial_update'})),
    path('delete/<int:pk>', PetAdoptView.as_view({'delete': 'destroy'})),

    # 查询
    path('get/<int:pk>', PetAdoptInformationView.as_view({'get': 'retrieve'})),
    path('list', PetAdoptInformationView.as_view({'get': 'list'})),

]
