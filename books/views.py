from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from books.forms import EbookForm, AuthorForm
from books.models import Ebook


class BookListView(ListView):
    template_name='books/book_list.html'
    model = Ebook

class BookDetailView(DetailView):
    template_name = 'books/book_details.html'
    model = Ebook
    pk_url_kwarg = 'ebook_slug'

class EbookCreateView(CreateView):
    form_class = EbookForm
    template_name = 'books/add_book_form.html'
    success_url = '/books/'

class AuthorCreateView(CreateView):
    form_class = AuthorForm
    template_name = 'books/add_author_form.html'
    success_url = '/books/'