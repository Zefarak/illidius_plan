from django import forms
from .models import *


class GameForm(forms.ModelForm):
    season = forms.ModelChoiceField(queryset=Season.objects.all(), widget=forms.HiddenInput())
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Game
        fields = '__all__'
        exclude = ['total_games', ]

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'