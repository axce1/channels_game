from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import *
from ..serializers import *


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PlayerGameViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Game.get_games_for_player(self.request.user)
        serializer = GameSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializer.data)
