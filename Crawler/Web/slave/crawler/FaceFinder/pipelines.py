# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#Pipeline based on the one from https://github.com/rolando/dirbot-mysql/

from datetime import datetime
from hashlib import md5
import logging
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi



class FacefinderPipeline(object):
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
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

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
            logging.debug("Item stored in db: %s %r" % (url, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.error(failure)
