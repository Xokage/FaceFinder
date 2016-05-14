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

from django.test import TestCase
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from slave.forms import AddJobForm, AddPersonForm, PhotoUploadForm, DataFilterForm, GraphMinOccurrenceForm
from slave.models import Person

import shutil

class AddJobFormTestCase(TestCase):

    def setUp(self):
        self.main_picture = 'slave/tests/test_assets/img/MainPicture.jpg'
        Person.objects.create(name="BraisTest", lastname="MareloTest", age=42 ,main_picture=File(open(self.main_picture,'r')))

    def test_valid_form(self):
        form_data = {'name': 'Brais', 'lastname':'Marelo','twitter_url':'http://mobile.twitter.com/something'}
        form = AddJobForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'name': 'PepeNonExiste', 'lastname':'QueVaNonExiste','twitter_url':'http://mobile.twitter.com/something'}
        form = AddJobForm(data=form_data)
        self.assertFalse(form.is_valid())

    def tearDown(self):
        shutil.rmtree('FaceFinder/media/pictures/BraisTest MareloTest')


class AddPersonFormTestCase(TestCase):

    def setUp(self):
        self.main_picture = File(open('slave/tests/test_assets/img/MainPicture.jpg','r'))
        Person.objects.create(name="BraisTest", lastname="MareloTest", age=42 ,main_picture=self.main_picture)

    def test_valid_form(self):
        image = File(open('slave/tests/test_assets/img/MainPicture.jpg','rb'))
        form_data = {'name': 'BraisTest', 'lastname':'MareloTest','age':42}
        form_file = {'main_picture': SimpleUploadedFile(image.name, image.read())}
        form = AddPersonForm(form_data, form_file)
        self.assertTrue(form.is_valid())

    def test_save_form(self):
        image = File(open('slave/tests/test_assets/img/MainPicture.jpg','rb'))
        form_data = {'name': 'Pepe', 'lastname':'Livingstone','age':42}
        form_file = {'main_picture': SimpleUploadedFile(image.name, image.read())}
        form = AddPersonForm(form_data, form_file)
        self.assertTrue(form.is_valid())
        form.save()
        obtained_person = Person.objects.get(name='Pepe')
        self.assertEquals('Livingstone',obtained_person.lastname)

    def tearDown(self):
        Person.objects.all().delete()


class PhotoUploadFormTestCase(TestCase):

    def test_valid_form(self):
        image = File(open('slave/tests/test_assets/img/MainPicture.jpg','rb'))
        form_file = {'file': SimpleUploadedFile(image.name, image.read())}
        form = PhotoUploadForm(None,form_file)
        self.assertTrue(form.is_valid())

class DataFilterFormTestCase(TestCase):

    def test_valid_form(self):
        form_data = {'person_name': 'Pepe', 'account_name':'conta','min_occurrence':1}
        form = DataFilterForm(form_data)
        self.assertTrue(form.is_valid())

class GraphMinOccurrenceFormTestCase(TestCase):

    def test_valid_form(self):
        form_data = {'min_occurrence':1}
        form = GraphMinOccurrenceForm(form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'min_occurrence':-1}
        form = GraphMinOccurrenceForm(form_data)
        self.assertFalse(form.is_valid())
