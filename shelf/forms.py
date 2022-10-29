from django import forms
from django.core.exceptions import ValidationError

from shelf.models import Person, Studio


def min_year(value):
    if value < 1900:
        raise ValidationError('No chba cos jest nie tak!!!')

class MovieAddForm(forms.Form):
    title = forms.CharField(max_length=123)
    year = forms.IntegerField(validators=[min_year])
    director = forms.ModelChoiceField(
        queryset=Person.objects.all(), widget=forms.RadioSelect)
    studio = forms.ModelChoiceField(
        queryset=Studio.objects.all()
    )

    def clean(self):
        cleaned_data = super().clean()
        studio = cleaned_data['studio']
        year = cleaned_data['year']
        if studio.year > year:
            raise ValidationError("rok produkcji filmu nie moze być mniejszy niż rok założenia studia")
        return cleaned_data




class StudioAddForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = "__all__"