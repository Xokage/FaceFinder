#####Tables
import django_tables2 as tables
from .models import TwitterItem
from django.utils.safestring import mark_safe
from django.utils.html import escape

class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe('<img src="%s" style="width:150px;height:150px;"/>' % escape(value[:value.find(':small')]))

class TweetColumn(tables.Column):
    def render(self, value):
        return mark_safe('<a target="_blank" href="%s" >Tweet</a>' % escape(value))

class DataTable(tables.Table):
    imageUrl = ImageColumn()
    tweetUrl = TweetColumn()

    class Meta:
        model = TwitterItem
        fields = ("account", "tweetUrl", "occurrence", "imageUrl")
        sequence = ("account", "tweetUrl", "occurrence", "imageUrl")

class JobTable(tables.Table):
    start_time = tables.Column()
    id  = tables.Column()
    spider = tables.Column()
    
