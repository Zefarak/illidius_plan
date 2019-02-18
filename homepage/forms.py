from django import forms
from .models import Contact

#  data-wow-duration="500ms" data-wow-delay=".6s"


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Your name',
                                                                   'class': 'form-group wow fadeInDown',
                                                                   'data-vow-duration': '500ms',
                                                                   'data-vow-delay': '.6s',
                                                                   }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Your Email',
                                                                      'class': 'form-group wow fadeInDown',
                                                                      'data-vow-duration': '500ms',
                                                                      'data-vow-delay': '.8s',
                                                                   }))
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Subject',
                                                                      'class': 'form-group wow fadeInDown',
                                                                      'data-vow-duration': '500ms',
                                                                      'data-vow-delay': '1s',
                                                                    }))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Message',
                                                                     'class':'form-group wow fadeInDown',
                                                                     'data-vow-duration': '500ms',
                                                                     'data-vow-delay': '1.2s',
                                                                    }))

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['day_added', 'is_readed']
