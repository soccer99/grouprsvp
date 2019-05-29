from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField


class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Team(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="owned_teams", on_delete=models.SET_NULL, blank=True, null=True
    )
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    name = models.CharField(max_length=120)
    players = models.ManyToManyField(Player, through="Membership")
    logo = models.ImageField(blank=True, null=True)
    default_tz = models.CharField(max_length=32, default="America/Los_Angeles")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField()
    position = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.player, self.team)


# Games


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=120)
    address = JSONField(default=dict)
    description = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team.name + " : " + str(self.date)

    class Meta:
        ordering = ["date"]


class PlayerAttending(models.Model):
    YES = "yes"
    NO = "no"
    MAYBE = "maybe"
    going_choices = (
        (YES, "Yes"),
        (NO, "No"),
        (MAYBE, "Maybe"),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rsvp_date = models.DateTimeField(auto_now_add=True)
    going = models.CharField(max_length=12, choices=going_choices, default=MAYBE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


# Messaging


class TeamMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    players = models.ManyToManyField(Player)
    content = models.TextField()
    date_to_send = models.DateTimeField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
