from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic import TemplateView

from ..models import Game


class HomeView(TemplateView):
    template_name = 'home.html'


class CreateUserView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(CreateUserView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username,
                                password=password)
        login(self.request, new_user)
        return valid


class LobbyView(LoginRequiredMixin, TemplateView):
    template_name = 'components/lobby/lobby.html'

    def dispatch(self, request, *args, **kwargs):
        return super(LobbyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(LobbyView, self).get_context_data(**kwargs)
        available_games = [{'creator': game.creator.username, 'id': game.pk}
                           for game in Game.get_available_games()]
        player_games = Game.get_games_for_player(self.request.user)

        return ctx
