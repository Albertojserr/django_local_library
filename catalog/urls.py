from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^libros/$', views.BookListView.as_view(), name='libros'),
    re_path(r'^libro/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='libro-detail'),
    re_path(r'^autores/$', views.AuthorListView.as_view(), name='autores'),
    re_path(r'^autor/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='autor-detail'),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^borrowed/$', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    re_path(r'^libro/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
    re_path(r'^autor/create/$', views.AuthorCreate.as_view(), name='author_create'),
    re_path(r'^autor/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^autor/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    re_path(r'^libro/create/$', views.BookCreate.as_view(), name='book_create'),
    re_path(r'^libro/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    re_path(r'^libro/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]
