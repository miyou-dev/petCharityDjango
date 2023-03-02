from django.contrib import admin

from adopt.models import PetAdopt


@admin.register(PetAdopt)
class AdoptAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'title', 'create_time')
    search_fields = ['pet__name', 'title', 'description', 'requirements']
    list_filter = ['pet__breed', 'pet__sex']
