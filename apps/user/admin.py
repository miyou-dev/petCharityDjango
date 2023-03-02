from django.contrib import admin

from user.models import Contact, User, UserFollowing, UserCollect


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'mail', 'qq', 'wechat')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'phone', 'sex', 'identity', 'area', 'introduction', 'create_time')


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'followers', 'following', 'time')


@admin.register(UserCollect)
class UserCollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'collect_category', 'collect_id', 'collect_time')
    list_filter = ['collect_category']
