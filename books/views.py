from django.shortcuts import render
from django.views.generic import ListView, DetailView
from books.models import Ebook


class BookListView(ListView):
    template_name='books/book_list.html'
    model = Ebook

class BookDetailView(DetailView):
    template_name = 'books/book_details.html'
    model = Ebook
    pk_url_kwarg = 'ebook_slug'

