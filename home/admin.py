from django.contrib import admin
from .models import faq, AdminUser, announcement, BadWord

class teamAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    search_fields = ['username']
    list_filter = ['role']

class announcementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    search_fields = ['author']
    list_filter = ['author']    

class faqAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

class BadWordAdmin(admin.ModelAdmin):
    list_display = ['word']
    search_fields = ['word']

admin.site.register(announcement, announcementAdmin)
admin.site.register(AdminUser, teamAdmin)
admin.site.register(faq, faqAdmin)
admin.site.register(BadWord, BadWordAdmin)