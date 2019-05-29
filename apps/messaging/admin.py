from django.contrib import admin

from .models import MO, MTRequest, MTSent, EmailMessage

@admin.register(MO)
class MOAdmin(admin.ModelAdmin):
    list_display = ("phone_number",)


@admin.register(MTRequest)
class MTRequestAdmin(admin.ModelAdmin):
    list_display = ("phone_number",)
