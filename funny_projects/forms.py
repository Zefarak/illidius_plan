from django import forms

from .models import GymPerson


class GymPersonForm(forms.ModelForm):

    class Meta:
        model = GymPerson
        fields = '__all__'
        exclude = ['name', 'slugfield']

    def __init__(self, *args, **kwargs):
        super(GymPersonForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
