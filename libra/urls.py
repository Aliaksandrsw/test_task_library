from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('', views.BaseViews.as_view(), name='start'),
    path('reader/', views.BookListView.as_view(), name='book_list'),
    path('reader/my-books/', views.MyBooksView.as_view(), name='my_books'),
    path('libra/debtors/',  views.DebtorsListView.as_view(), name='debtors_list'),
]