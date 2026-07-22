from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import BotMessage


@admin.register(BotMessage)
class BotMessageAdmin(ModelAdmin):
    list_display = ['channel', 'external_user_id', 'direction', 'text', 'created_at']
    list_filter = ['channel', 'direction']
    search_fields = ['external_user_id', 'text']
    readonly_fields = [f.name for f in BotMessage._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
