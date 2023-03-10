from django.urls import path, include
from unicodedata import name

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author, name='author-detail'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('mybooks/new', views.BookByUserCreateView.as_view(), name='my-borrowed-new'),
    path('mybooks/<uuid:pk>', views.BookByUserDetailView.as_view(), name='my-book'),
    path('mybooks/<uuid:pk>/update', views.BookByUserUpdateView.as_view(), name='my-book-update'),
    path('mybooks/<uuid:pk>/delete', views.BookByUserDeleteView.as_view(), name='my-book-delete'),

]
