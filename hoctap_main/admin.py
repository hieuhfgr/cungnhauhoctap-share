from django.contrib import admin
from .models import post, QnA, chatQnA, test

class postAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title', 'author', 'is_verify', 'is_publish')
    search_fields = ['post_id']
    list_filter = ['is_verify']

class testAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'title', 'author', 'is_verify', 'is_publish')
    search_fields = ['test_id']
    list_filter = ['is_verify']

class ChatQnAInline(admin.TabularInline):
    model = chatQnA

class qnaAdmin(admin.ModelAdmin):
    list_display = ('post', 'is_finished')
    search_fields = ['post']
    list_filter = ['is_finished']
    inlines = [ChatQnAInline]

admin.site.register(post, postAdmin)
admin.site.register(test, testAdmin)
admin.site.register(QnA, qnaAdmin)