from django.contrib import admin
from .models import ToDo, news

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', "is_finished")
    search_fields = ['user']
    
class newsAdmin(admin.ModelAdmin):
    list_display = ['content']
    search_fields = ['content']

admin.site.register(ToDo, ToDoAdmin)
admin.site.register(news, newsAdmin)