from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

from books.forms import EbookForm, AuthorForm, SignUpForm
from books.models import Ebook, Gendre
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'books/signup.html'


class BookListView(ListView):
    template_name='books/book_list.html'
    model = Ebook

class BookDetailView(DetailView):
    template_name = 'books/book_details.html'
    model = Ebook
    pk_url_kwarg = 'ebook_slug'


class HomePageView(View):
    def get(self,request,):
        ebooks=Ebook.objects.all()
        gendres = Gendre.objects.all().order_by('name')
        gendre_count = Gendre.objects.annotate(total_gendre=Count('ebook')).order_by('name')
        last5_ebooks = Ebook.objects.order_by('-created')[0:5]
        discount_books = Ebook.objects.filter(discount_percent__gt=0)[0:5]

        return render(request,'books/home.html',{'gendres':gendres,
                                                 'gendre_count':gendre_count,
                                                 'ebooks':ebooks,
                                                 'last5_ebooks':last5_ebooks,
                                                 'discount_books':discount_books
                                                 })


class GendreBooksView(View):
    def get(self,request,gendre_slug=None):
        gendre_books = Ebook.objects.all()
        if gendre_slug:
            gendre= Gendre.objects.get(slug=gendre_slug)
            gendre_books=gendre_books.filter(gendre=gendre)
        return render(request,'books/gendre_list.html',{'gendre_books':gendre_books})



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