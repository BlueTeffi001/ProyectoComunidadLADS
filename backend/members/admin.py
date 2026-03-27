from django.contrib import admin
from .models import MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "main_li", "status", "role", "birthday")
    list_filter = ("status", "role", "main_li")
    search_fields = ("user__username",)