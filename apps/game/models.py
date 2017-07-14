from channels import Group
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Game(models.Model):

    creator = models.ForeignKey(User, related_name='creator')
    opponent = models.ForeignKey(User, related_name='opponent',
                                 null=True, blank=True)
    winner = models.ForeignKey(User, related_name='winner',
                               null=True, blank=True)
    cols = models.IntegerField(default=6)
    rows = models.IntegerField(default=6)
    current_turn = models.ForeignKey(User, related_name='current_turn')

    completed = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modifed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Game #{}'.format(self.pk)

    @staticmethod
    def get_available_games():
        return Game.objects.filter(opponent=None, completed=None)

    @staticmethod
    def create_count(user):
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return Game.objects.filter(Q(opponent=user) | Q(creator=user))

    @staticmethod
    def get_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            pass

    @staticmethod
    def create_new(user):
        new_game = Game(creator=user, current_turn=user)
        new_game.save()

        for row in range(new_game.rows):
            for col in range(new_game.cols):
                new_square = GameSquare(
                    game=new_game,
                    row=row,
                    col=col
                )
                new_square.save()
        new_game.add_log('Game created by {}'
                         .format(new_game.creator.username))
        return new_game

    def add_log(self, text, user=None):
        return GameLog(game=self, text=text, player=user).save()

    def get_all_game_squares(self):
        return GameSquare.objects.filter(game=self)

    def get_game_square(self, row, col):
        try:
            return GameSquare.objects.get(game=self, cols=col, rows=row)
        except GameSquare.DoesNotExist:
            return None

    def get_square_by_coords(self, coords):
        try:
            square = GameSquare.objects.get(row=coords[1],
                                            col=coords[0],
                                            game=self)
            return square
        except GameSquare.DoesNotExist:
            return None

    def get_game_log(self):
        return GameLog.objects.filter(game=self)

    def send_game_update(self):

        from serializers import GameSquareSerializer,\
            GameLogSerializer, GameSerializer

        squares = self.get_all_game_squares()
        square_serializer = GameSquareSerializer(squares, many=True)

        log = self.get_game_log()
        log_serializer = GameLogSerializer(log, many=True)

        game_serializer = GameSerializer(self)

        message = {'game': game_serializer.data,
                   'log': log_serializer.data,
                   'squares': square_serializer.data}

        game_group = 'game-{}'.format(self.id)
        Group(game_group).send({'text': json.dumps(message)})

    def next_player_turn(self):
        self.current_turn = self.creator\
            if self.current_turn != self.creator else self.opponent
        self.save()

    def mark_complete(self, winner):
        self.winner = winner
        self.completed = timezone.now()
        self.save()


class GameSquare(models.Model):
    STATUS_TYPES = (
        ('Free', 'Free'),
        ('Selected', 'Selected'),
        ('Surrounding', 'Surrounding')
    )
    game = models.ForeignKey(Game)
    owner = models.ForeignKey(User, null=True, blank=True)
    status = models.CharField(choices=STATUS_TYPES,
                              max_length=25,
                              default='Free')
    row = models.IntegerField()
    col = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - ({}, {})'.format(self.game,
                                      self.col,
                                      self.row)

    @staticmethod
    def get_by_id(id):
        try:
            return GameSquare.objects.get(pk=id)
        except GameSquare.DoesNotExist:
            return None

    def get_surrounding(self):
        ajecency_matrix = [(i, j) for i in (-1, 0, 1)
                           for j in (-1, 0, 1) if not (i == j == 0)]

        results = []
        for dx, dy in ajecency_matrix:
            if 0 <= (self.col + dy) < self.game.cols\
                    and 0 <= (self.row + dx) < self.game.rows:
                results.append((self.col + dy, self.row + dx))
        return results

    def claim(self, status_type, user):
        self.owner = user
        self.status = status_type
        self.save(update_fields=['status', 'owner'])

        surrounidng = self.get_surrounding()

        for coords in surrounidng:
            square = self.game.get_square_by_coords(coords)

            if square and square.status == 'Free':
                square.status = 'Surrounding'
                square.owner = user
                square.save()

        self.game.add_log('Square claimed at ({}, {}) by {}'
                          .format(self.col, self.row, self.owner.username))

        if self.game.get_all_game_squares().filter(status='Free'):
            self.game.next_player_turn()
        else:
            self.game.mark_complete(winner=user)
        self.game.send_game_update()


class GameLog(models.Model):
    game = models.ForeignKey(Game)
    text = models.CharField(max_length=300)
    player = models.ForeignKey(User, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Game #{} Log'.format(self.game.id)
