from django.contrib import admin
#
from pet.models import PetBreed, PetImage, Pet, PetImageMap


@admin.register(PetBreed)
class PetBreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'race', 'path', 'variety')
    search_fields = ['name', 'variety']
    list_filter = ['race', 'variety']


admin.site.register(PetImage)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed', 'sex', 'name', 'weight', 'birth', 'create_time', 'user')
    search_fields = ['name']
    list_filter = ['user', 'sex', 'breed']


@admin.register(PetImageMap)
class PetImageMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'image', 'cover')
