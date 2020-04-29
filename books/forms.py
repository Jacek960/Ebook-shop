from django import forms
from books.models import Ebook, Autor


class EbookForm(forms.ModelForm):
    class Meta:
        model=Ebook
        fields = ['name','description','autor','publisher','gendre','price','vat','discount_percent','format','image','file_upload_1','file_upload_2']
        # widgets={
        #     'advantages':forms.CheckboxSelectMultiple,
        #     'surroundings': forms.CheckboxSelectMultiple,
        # }
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