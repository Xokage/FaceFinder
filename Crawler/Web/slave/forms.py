from django import forms

class AddJobForm(forms.Form):
    person = forms.CharField(label='Nome da persoa', max_length=100)
    twitter_url = forms.CharField(label='Url de twitter (recorda que ten que ser de mobile.twitter.com)', max_length=200)
    image_directory = forms.CharField(label='Subdirectorio das imaxes a comparar', max_length=100)
    downloads_directory = forms.CharField(label='Subdirectorio de descarga de imaxes', max_length=100)
