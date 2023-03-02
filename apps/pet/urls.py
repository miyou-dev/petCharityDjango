from django.urls import path

from pet.views.pet_breed_view import PetBreedView
from pet.views.pet_image_view import PetImageView
from pet.views.pet_information_view import PetInformationView
from pet.views.pet_view import PetView

urlpatterns = [

    path('breed/<int:pk>', PetBreedView.as_view({'get': 'retrieve'})),
    path('breed/list', PetBreedView.as_view({'get': 'list'})),

    # 宠物图片
    path('image/get/<int:pk>', PetImageView.as_view({'get': 'retrieve'})),
    path('image/create', PetImageView.as_view({'post': 'create'})),
    path('image/<int:pk>', PetImageView.as_view({'get': 'get'})),
    # 宠物 查
    path('pet/<int:pk>', PetInformationView.as_view({'get': 'retrieve'})),
    path('pet/list', PetInformationView.as_view({'get': 'list'})),

    # 宠物 增 删 改
    path('pet/create', PetView.as_view({'post': 'create'})),
    path('pet/delete/<int:pk>', PetView.as_view({'delete': 'destroy'})),
    path('pet/partialUpdate/<int:pk>', PetView.as_view({'patch': 'partial_update'})),

]
