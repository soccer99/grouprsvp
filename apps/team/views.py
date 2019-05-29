from rest_framework import viewsets

from .models import Team, Game, Player, Location
from .serializers import PlayerSerializer, GameSerializer, TeamSerializer, LocationSerializer
from .permissions import IsTeamAdminOrReadOnly


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    permission_classes = [IsTeamAdminOrReadOnly]

    def get_queryset(self):
        # Only return players that exist in a team the user is an admin/owner of
        return Player.objects.filter(id__in=set(i[0] for i in self.request.user.owned_teams.values_list("players")))


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [IsTeamAdminOrReadOnly]

    def get_queryset(self):
        # Only return games that exist for a team the user is an admin/owner/player in

        # TODO : write query for games
        return Game.objects.all()


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsTeamAdminOrReadOnly]

    def get_queryset(self):
        # Only return teams that the user is an admin/owner/player in

        # TODO : write query for teams
        return Team.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsTeamAdminOrReadOnly]
