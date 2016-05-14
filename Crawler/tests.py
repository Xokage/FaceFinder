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


import unittest, os, errno, shutil, urllib
from FaceFinder.spiders.twitter_spider import TwitterSpider 
from FaceFinder.test.test_util import fake_response_from_file


class TwitterSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = TwitterSpider(start_url='http://mobile.twitter.com/neiltyson',image_dir='image_dir',downloads_dir='downloads_dir',person_id='0')
        try:
            os.makedirs('image_dir')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def tearDown(self):
        shutil.rmtree('downloads_dir')

    def _test_parse_item_results(self, results, expected_length):
        count = 0
        for req in results:
            count = count + 1
        self.assertEqual(count, expected_length)

    def test_parse(self):
        #this directory SHOULD NOT exist, it should have been cleaned, so if it exists throw exception.
        os.makedirs('downloads_dir')
        #45 results = 24 mentions + 20 tweets with images + 1 next page of tweets
        results = self.spider.parse(fake_response_from_file('html/Neil deGrasse Tyson.html','http://mobile.twitter.com/neiltyson'))
        self._test_parse_item_results(results, 45)

    def test_compare_images(self):
        #THIS TEST FAILS ON CIRCLE-CI SO IT WONT RUN ON IT (hangs, dunno why)
        self.spider.start_requests()
        imageBillAPath = 'file:' + urllib.pathname2url(os.path.join('FaceFinder','test','images','BillA.jpg'))
        imageBillBPath = 'file:' + urllib.pathname2url(os.path.join('FaceFinder','test','images','BillB.jpg'))
        imageNonBillAPath = 'file:' + urllib.pathname2url(os.path.join('FaceFinder','test','images','NonBillA.jpg'))
        imageNonBillBPath = 'file:' + urllib.pathname2url(os.path.join('FaceFinder','test','images','NonBillB.jpg'))
        self.assertGreater(self.spider.compare_image(imageBillAPath)[0][1],1)
        self.assertGreater(self.spider.compare_image(imageBillBPath)[0][1],1)
        self.assertLess(self.spider.compare_image(imageNonBillAPath)[0][1],0)
        self.assertLess(self.spider.compare_image(imageNonBillBPath)[0][1],0)
        self.spider.closed('test finished')


if __name__ == '__main__':
    unittest.main()

