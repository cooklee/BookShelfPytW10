from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from shelf.models import Person, Studio, Comment


def min_year(value):
    if value < 1900:
        raise ValidationError('No chba cos jest nie tak!!!')

class MovieAddForm(forms.Form):
    title = forms.CharField(max_length=123)
    year = forms.IntegerField(validators=[min_year])
    director = forms.ModelChoiceField(
        queryset=Person.objects.all(), widget=forms.RadioSelect)
    studio = forms.ModelChoiceField(
        queryset=Studio.objects.all(), required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        studio = cleaned_data['studio']
        year = cleaned_data['year']
        if studio is not None and studio.year > year:
            raise ValidationError("rok produkcji filmu nie moze być mniejszy niż rok założenia studia")
        return cleaned_data




class StudioAddForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = "__all__"


class CommentAddForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(
        max_length=100, widget=forms.PasswordInput
    )


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=120, widget=forms.PasswordInput)
    password2= forms.CharField(max_length=120, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('Hasła nie są takie same!!!')
