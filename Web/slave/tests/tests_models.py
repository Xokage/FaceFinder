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
from slave.models import Person, Picture
import os, shutil

class PersonTestCase(TestCase):

    def setUp(self):
        self.filename = 'slave/tests/test_assets/img/MainPicture.jpg'
        Person.objects.create(name="BraisTest", lastname="MareloTest", age=42 ,main_picture=File(open(self.filename,'r')))

    def test_upload_main_picture(self):
        """Person's main picture is correctly uploaded"""

        person = Person.objects.get(name="BraisTest")
        expected_file = 'FaceFinder/media/pictures/BraisTest MareloTest/main_picture/' + self.filename
        self.assertTrue(os.path.isfile(expected_file))

    def test_correct_string(self):
        """Person object converts to string correctly"""

        person = Person.objects.get(name="BraisTest")
        self.assertEqual('BraisTest MareloTest',str(person))

    def tearDown(self):
        shutil.rmtree('FaceFinder/media/pictures/BraisTest MareloTest')

class PictureTestCase(TestCase):

    def setUp(self):
        self.main_picture = 'slave/tests/test_assets/img/MainPicture.jpg'
        self.some_picture = 'slave/tests/test_assets/img/PersonPicture.jpg'
        Person.objects.create(name="BraisTest", lastname="MareloTest", age=42 ,main_picture=File(open(self.main_picture,'r')))
        self.test_person = Person.objects.get(name="BraisTest")
        Picture.objects.create(file=File(open(self.some_picture,'r')),person=self.test_person)

    def test_upload_picture_of_person(self):
        """Picture where some person appears in is correctly uploaded"""

        expected_file = 'FaceFinder/media/pictures/BraisTest MareloTest/reference_pictures/' + self.some_picture
        self.assertTrue(os.path.isfile(expected_file))

    def tearDown(self):
        shutil.rmtree('FaceFinder/media/pictures/BraisTest MareloTest')
    
