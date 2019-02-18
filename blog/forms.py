from django import forms
from .models import *
from PIL import Image

MAX_FILE_SIZE = 2*1024*1024


class PostCreate(forms.ModelForm):
    title = forms.CharField(label="Τίτλος 'Αθρου", widget=forms.TextInput(attrs={'onkeyup':"myTitle()",}))
    lead_content = forms.CharField(label='Πρώτα Σχόλια', widget=forms.Textarea(attrs={'onkeyup':"myLeadCon()",}))
    content = forms.CharField(label='Βασικό Κείμενο', widget=forms.Textarea(attrs={'onkeyup':"myCon()",}))
    #content = forms.CharField(label='Βασικό Κείμενο', widget=FroalaEditor(attrs={'onkeyup':"myCon()",}))
    #user = forms.ChoiceField(widget=forms.HiddenInput())
    #publish = forms.DateTimeField(widget=forms.DateTimeField())

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['publish','user']


class PostTagForm(forms.ModelForm):

    class Meta:
        model = PostTags
        fields = '__all__'

class PostCategoryForm(forms.ModelForm):

    class Meta:
        model = PostCategory
        fields = '__all__'


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(attrs={'onkeyup':"myTitle()",}))
    content = forms.CharField(widget=forms.Textarea(attrs={'onkeyup':"myContent()",}))

    class Meta:
        model = Post
        fields = '__all__'

    def save(self):
        photo = super(PhotoForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.name)
        return photo


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file._size > MAX_FILE_SIZE:
                raise forms.ValidationError('This file is bigger than 2 mb')
            return file
        else:
            raise forms.ValidationError('Something wrong with this file')
