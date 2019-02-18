from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import ListView, CreateView

import datetime
from .models import *
from .forms import GameForm


def homepage(request):
    season = Season.objects.filter(active=True).last()
    players = PlayerSeason.objects.filter(season=season)
    games = Game.objects.filter(season=season)[:20]
    form = GameForm(request.POST or None, initial={'date': datetime.datetime.now(),
                                                   'season': season,
                                                   })

    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('backgammon:homepage'))
    context = locals()
    return render(request, 'tim/backgammon_home.html', context)


def celebration(request):

    return render(request, 'tim/back_cele.html')