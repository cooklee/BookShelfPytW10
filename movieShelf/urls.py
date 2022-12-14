"""movieShelf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from shelf import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name='base.html'), name='index'),
    path('addPerson/', views.CreatePersonView.as_view(), name='create_person'),
    path('listPerson/', views.ListPersonView.as_view(), name='list_person'),
    path('addMovie/', views.AddMovieView.as_view(), name='create_movie'),
    path('listMovie/', views.ListMovieView.as_view(), name='list_movie'),
    path('AddStudio/', views.AddStudioView.as_view(), name='add_stuido'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='detail_movie'),
    path('add_comment/<int:movie_pk>/', views.AddCommentView.as_view(), name='add_comment'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register')
]
