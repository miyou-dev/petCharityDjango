from django.contrib import admin

from donate.models import PetDonate, PetDonateImageMap, PetDonationList


@admin.register(PetDonate)
class PetDonateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'breed', 'sex', 'sex', 'admin', 'create_time', 'publish_time')
    search_fields = ['name', 'description']
    list_filter = ['sex', 'breed']


@admin.register(PetDonateImageMap)
class PetDonateImageMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'donate', 'image', 'cover')


@admin.register(PetDonationList)
class PetDonationListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'donate', 'amount', 'order', 'donate_time')
    search_fields = ['user', 'donate']
    list_filter = ['user', 'donate']
