from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from books.forms import EbookForm, AuthorForm
from books.models import Ebook


class BookListView(ListView):
    template_name='books/book_list.html'
    model = Ebook

class BookDetailView(DetailView):
    template_name = 'books/book_details.html'
    model = Ebook
    pk_url_kwarg = 'ebook_slug'

class EbookCreateView(PermissionRequiredMixin,CreateView):
    form_class = EbookForm
    template_name = 'books/add_book_form.html'
    success_url = '/books/'
    permission_required = 'books.add_ebook'

class AuthorCreateView(PermissionRequiredMixin,CreateView):
    form_class = AuthorForm
    template_name = 'books/add_author_form.html'
    success_url = '/books/'
    permission_required = 'books.add_autor'

class EbookUpdate(PermissionRequiredMixin,UpdateView):
    model = Ebook
    form_class = EbookForm
    template_name = 'books/add_book_form.html'
    success_url = '/books/'
    permission_required = 'books.change_ebook'

class EbookDelete(PermissionRequiredMixin,DeleteView):
    model = Ebook
    template_name = 'books/ebook_delete.html'
    success_url = '/books/'
    permission_required = 'books.delete_ebook'