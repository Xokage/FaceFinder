from django import forms
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Person

class AddJobForm(forms.Form):
    name = forms.CharField(label='Nome da persoa', max_length=100)
    lastname = forms.CharField(label='Apelidos da persoa', max_length=100)
    twitter_url = forms.CharField(label='Url de twitter (recorda que ten que ser de mobile.twitter.com)', max_length=200)
    
    def clean(self):
        data = self.cleaned_data
        name = self.cleaned_data.get('name', None)
        lastname = self.cleaned_data.get('lastname',None)
        if name and lastname:
            try:
                person = Person.objects.get(Q(name__contains=data['name']) | Q(lastname__contains=data['lastname']))
            except ObjectDoesNotExist:
                raise forms.ValidationError("Persoa non atopada!")
        return data

class AddPersonForm(forms.ModelForm):
    name = forms.CharField(label='Nome da persoa', max_length=100)
    lastname = forms.CharField(label='Apelidos da persoa', max_length=100)
    age = forms.IntegerField(label='Idade', min_value=1)
    main_picture = forms.ImageField(label='Fotografia')
    
    class Meta:
        model = Person
        fields = ("name", "lastname", "age", "main_picture")


class PhotoUploadForm(forms.Form):
    #Keep name to 'file' because that's what Dropzone is using
    file = forms.ImageField(required=True)

