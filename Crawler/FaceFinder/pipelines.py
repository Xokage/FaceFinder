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

#Pipeline based on the one from https://github.com/rolando/dirbot-mysql/

import logging
from twisted.enterprise import adbapi



class FacefinderPipeline(object):
    @staticmethod
    def process_item(self, item, spider):
        return item


class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        url = item['imageUrl']

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM slave_twitteritem WHERE imageUrl = %s
        )""", (url, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE slave_twitteritem
                SET account=%s, imageUrl=%s, tweetUrl=%s, occurrence=%s
                WHERE imageUrl=%s
            """, (item['account'], item['imageUrl'], item['tweetUrl'], item['occurrence'], url))
            logging.debug("Item updated in db: %s %r" % (url, item))

        else:
            conn.execute("""
                INSERT INTO slave_twitteritem (account, imageUrl, tweetUrl, occurrence)
                VALUES (%s, %s, %s, %s)
            """, (item['account'], item['imageUrl'], item['tweetUrl'], item['occurrence']))
            if item['person_id']:
                conn.execute("""
                    INSERT INTO slave_twitteritem_people (twitteritem_id, person_id)
                    VALUES ((SELECT id FROM slave_twitteritem WHERE imageUrl = %s), %s)
                """, (item['imageUrl'], item['person_id']))
            logging.debug("Item stored in db: %s %r" % (url, item))

    @staticmethod
    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.error(failure)
