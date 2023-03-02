from django.urls import path

from address.views import ProvinceView, CityView, AreaView

urlpatterns = [
    path('province/<int:pk>', ProvinceView.as_view({'get': 'retrieve'})),
    path('province/list', ProvinceView.as_view({'get': 'list'})),

    path('city/<int:pk>', CityView.as_view({'get': 'retrieve'})),
    path('city/list', CityView.as_view({'get': 'list'})),

    path('area/<int:pk>', AreaView.as_view({'get': 'retrieve'})),
    path('area/list', AreaView.as_view({'get': 'list'})),

]
