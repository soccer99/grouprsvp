from rest_framework import serializers

from .models import Team, Player, Game, Location


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "first_name", "last_name", "phone_number", "email")


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "admins", "players", "logo", "default_tz")


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("id", "team", "description", "date")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "address", "description")
