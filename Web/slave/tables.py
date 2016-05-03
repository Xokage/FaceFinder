#####Tables
import django_tables2 as tables
from .models import TwitterItem
from .models import Person
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings

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

class TextCancelJobUrlColumn(tables.Column):
    def render(self,value,record):
        return mark_safe('<a href="canceljob/{0}"><img src="{1}img/red_x_small.png" style="width:15px;height:15px;"/></a>'.format(str(record['id']),settings.STATIC_URL))

class TextDeletePersonUrlColumn(tables.Column):
    def render(self,value,record):
        return mark_safe('''<a href="delete_person/{0}" onClick="return confirm('Queres borrar a persoa?')"><img src="{1}img/red_x_small.png" style="width:25px;height:25px;"/></a>'''.format(str(record.id),settings.STATIC_URL))

class DataTable(tables.Table):
    imageUrl = ImageUrlColumn(orderable=False)
    tweetUrl = TweetColumn(orderable=False)

    class Meta:
        model = TwitterItem
        fields = ("account", "tweetUrl", "occurrence", "imageUrl")
        sequence = ("account", "tweetUrl", "occurrence", "imageUrl")

class JobTable(tables.Table):
    start_time = tables.Column()
    id  = tables.Column()
    spider = tables.Column()

class JobRunningTable(JobTable):
    cancel = TextCancelJobUrlColumn(orderable=False, empty_values=())    

class PersonTable(tables.Table):
    main_picture = ImageFilePersonColumn(orderable=False)
    name = TextPersonUrlColumn()
    class Meta:
        model = Person
        fields = ("name", "lastname", "age", "main_picture")
        sequence = ("name", "lastname", "age", "main_picture")

class PersonDeleteTable(PersonTable):
    delete = TextDeletePersonUrlColumn(orderable=False, empty_values=(), visible=True)

class PersonGraphTable(PersonTable):
    main_picture = ImageFileGraphColumn(orderable=False)
    name = TextGraphUrlColumn()
