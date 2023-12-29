from django.contrib import admin
from .models import Bookmark
# Register your models here.
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'active', 'active_update_timestamp', 'timestamp']
    readonly_fields = ['active_update_timestamp', 'timestamp']
    search_fields = ['user__username', 'movie__title']

admin.site.register(Bookmark, BookmarkAdmin)