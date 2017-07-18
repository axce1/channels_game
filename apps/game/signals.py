import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels import Group

from .models import *
from .serializers import *


@receiver(post_save, sender=Game)
def new_game_handler(**kwargs):
    if kwargs['created']:
        avail_game_list = Game.get_available_games()
        avail_serializer = GameSerializer(avail_game_list, many=True)
        Group('lobby').send({'text': json.DUMPS(AVAil_serializer.data)})
