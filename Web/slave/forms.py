# -*- coding: utf-8 -*-
#################################################################################
#   Facefinder: Crawl pictures based on known faces and extract information.    #
#   Copyright (C) 2016 Xoán Antelo Castro                                       #
#                                                                               #
#   This program is free software: you can redistribute it and/or modify        #
#   it under the terms of the GNU General Public License as published by        #
#   the Free Software Foundation, either version 3 of the License, or           #
#   (at your option) any later version.                                         #
#                                                                               #
#   This program is distributed in the hope that it will be useful,             #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#   GNU General Public License for more details.                                #
#                                                                               #
#   You should have received a copy of the GNU General Public License           #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#################################################################################

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


class DataFilterForm(forms.Form):
    person_name = forms.CharField(label='Persoa', max_length=100, required=False)
    account_name = forms.CharField(label='Conta', max_length=100, required=False)
    min_occurrence = forms.FloatField(label='Acerto', min_value=0, required=False)


class GraphMinOccurrenceForm(forms.Form):
    min_occurrence = forms.FloatField(label='Acerto', min_value=0)    
