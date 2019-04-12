from django.urls import path
from books import views


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.login, name='login'),
]