from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Game, GameSquare, GameLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')
