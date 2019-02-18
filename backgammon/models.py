from django.db import models
from  django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.


class Player(models.Model):
    title = models.CharField(unique=True, max_length=100)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    win_ratio = models.DecimalField(default=0, decimal_places=2, max_digits=50)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        players = self.playerseason_set.all()
        self.games_played = players.aggregate(Sum('games_played'))['games_played__sum'] if players else 0
        self.games_won = players.aggregate(Sum('games_won'))['games_won__sum'] if players else 0
        self.win_ratio = self.games_won/self.games_played if self.games_played > 0 else 0
        super(Player, self).save(*args, **kwargs)


class Season(models.Model):
    title = models.CharField(unique=True, max_length=50)
    active = models.BooleanField(default=True)
    minimum_games = models.IntegerField(default=30)
    date_start = models.DateField()
    date_end = models.DateField()
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class PlayerSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    games_played = models.PositiveIntegerField(default=0)
    games_won = models.PositiveIntegerField(default=0)
    win_ratio = models.DecimalField(default=0, decimal_places=2, max_digits=50)

    class Meta:
        ordering = ['-win_ratio']

    def __str__(self):
        return self.player.title

    def save(self, *args, **kwargs):
        games_home = Game.objects.filter(home=self, season=self.season)
        games_oppo = Game.objects.filter(opponent=self, season=self.season)
        print(games_oppo, games_home)
        self.games_played = games_home.aggregate(Sum('total_games'))['total_games__sum'] if games_home else 0
        self.games_played += games_oppo.aggregate(Sum('total_games'))['total_games__sum'] if games_oppo else 0
        self.games_won = games_home.aggregate(Sum('home_score'))['home_score__sum'] if games_home else 0
        self.games_won += games_oppo.aggregate(Sum('opponent_score'))['opponent_score__sum'] if games_oppo else 0
        self.win_ratio = self.games_won/self.games_played if self.games_played > 0 else 0
        super(PlayerSeason, self).save(*args, **kwargs)
        self.player.save()


class Game(models.Model):
    date = models.DateField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    home = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='home_player')
    opponent = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='opponent')
    home_score = models.PositiveIntegerField(default=0)
    opponent_score = models.PositiveIntegerField(default=0)
    total_games = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '%s - %s' % (self.home, self.opponent)

    def save(self, *args, **kwargs):
        self.total_games = self.home_score + self.opponent_score
        super(Game, self).save(*args, **kwargs)
        self.home.save()
        self.opponent.save()


@receiver(post_delete, sender=Game)
def update_data(sender, instance, **kwargs):
    instance.home.save()
    instance.opponent.save()