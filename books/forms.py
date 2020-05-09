from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from books.models import Ebook, Autor, Gendre, Publisher


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class EbookForm(forms.ModelForm):
    class Meta:
        model=Ebook
        fields = ['name','description','autor','publisher','gendre','price','vat','discount_percent','format','image','file_upload_1','file_upload_2']
        labels = {
            'name':'Tytuł',
            'description': 'Opis',
            'autor':'Autor',
            'publisher': 'Wydawca',
            'gendre':'Gatunek',
            'price':'Cena netto',
            'vat':'Stawka VAT',
            'discount_percent':'Rabat procentowy',
            'format':'Formaty pliku',
            'image': 'Okładka',
            'file_upload_1':'Plik 1',
            'file_upload_2': 'Plik 2',
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Autor
        fields = ['name']
        labels = {
            'name':'Imię i Nazwisko',

        }

class GendreForm(forms.ModelForm):
    class Meta:
        model=Gendre
        fields = ['name']
        labels = {
            'name':'Gatunek',
        }

class PublisherForm(forms.ModelForm):
    class Meta:
        model=Publisher
        fields = ['name']
        labels = {
            'name':'Nazwa',
        }