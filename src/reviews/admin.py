from django.contrib import admin
from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'user', 'content', 'timestamp', 'active']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    readonly_fields = ['content_object']

admin.site.register(Review, ReviewAdmin)