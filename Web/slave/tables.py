#####Tables
import django_tables2 as tables
from .models import TwitterItem
from .models import Person
from django.utils.safestring import mark_safe
from django.utils.html import escape

class ImageUrlColumn(tables.Column):
    def render(self, value):
        return mark_safe('<img src="%s" style="width:150px;height:150px;"/>' % escape(value[:value.find(':small')]))

class TweetColumn(tables.Column):
    def render(self, value):
        return mark_safe('<a target="_blank" href="%s" >Tweet</a>' % escape(value))

class ImageFileColumn(tables.Column):
    def render(self, value):
        return mark_safe('<img src="%s" style="width:150px;height:150px;"/>' % value.url)

class TextGraphUrlColumn(tables.Column):
    def render(self, value, record):
        return mark_safe('<a href="graphs/{0}">{1}</a>'.format(str(record.id), value))

class ImageFileGraphColumn(tables.Column):
    def render(self, value, record):
        return mark_safe('<a href="graphs/{0}"><img src="{1}" style="width:150px;height:150px;"/></a>'.format(str(record.id), value.url))

class ImageFilePersonColumn(tables.Column):
    def render(self, value, record):
        return mark_safe('<a href="person/{0}"><img src="{1}" style="width:150px;height:150px;"/></a>'.format(str(record.id), value.url))

class TextPersonUrlColumn(tables.Column):
    def render(self, value, record):
        return mark_safe('<a href="person/{0}">{1}</a>'.format(str(record.id), value))


class DataTable(tables.Table):
    imageUrl = ImageUrlColumn()
    tweetUrl = TweetColumn()

    class Meta:
        model = TwitterItem
        fields = ("account", "tweetUrl", "occurrence", "imageUrl")
        sequence = ("account", "tweetUrl", "occurrence", "imageUrl")

class JobTable(tables.Table):
    start_time = tables.Column()
    id  = tables.Column()
    spider = tables.Column()
    

class PersonTable(tables.Table):
    main_picture = ImageFilePersonColumn()
    name = TextPersonUrlColumn()
    class Meta:
        model = Person
        fields = ("name", "lastname", "age", "main_picture")
        sequence = ("name", "lastname", "age", "main_picture")


class PersonGraphTable(PersonTable):
    main_picture = ImageFileGraphColumn()
    name = TextGraphUrlColumn()
