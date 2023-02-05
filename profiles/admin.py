from django.contrib import admin
from .models import profile, notification

class profileAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'role', 'createdAt')
    search_fields=['username']
    list_filter = ('role', 'createdAt')

class notificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    search_fields=['user']
    list_filter = ['date']

admin.site.register(profile, profileAdmin)
admin.site.register(notification, notificationAdmin)