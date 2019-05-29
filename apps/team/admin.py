from django.contrib import admin

from .models import Player, Team, Membership, PlayerAttending, TeamMessage, Game, Location


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("team", "date")


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 2 # how many rows to show


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    inlines = (MembershipInline,)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "user")


@admin.register(TeamMessage)
class TeamMessageAdmin(admin.ModelAdmin):
    list_display = ("team", "date_to_send")


@admin.register(PlayerAttending)
class PlayerAttendingAdmin(admin.ModelAdmin):
    list_display = ("team", "player", "game", "get_going")

    def get_going(self, obj):
        return obj.get_going_display()

    get_going.short_description = 'Going'
