from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from shelf.forms import MovieAddForm, StudioAddForm, CommentAddForm, LoginForm, UserCreateForm
from shelf.models import Person, Movie


class CreatePersonView(View):

    def get(self, request):
        return render(request, 'addPerson.html')

    def post(self, request):
        imie = request.POST.get('first_name')
        nazwisko = request.POST.get('last_name')
        Person.objects.create(first_name=imie, last_name=nazwisko)
        return redirect('list_person')


class ListPersonView(View):
    def get(self, request):
        osoby = Person.objects.all()
        return render(request, 'PersonList.html', {'persons': osoby})


class ListMovieView(View):
    def get(self, request):
        filmy = Movie.objects.all()
        return render(request, 'movielist.html', {'movies': filmy})


class AddMovieView(View):

    def get(self, request):
        form = MovieAddForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = MovieAddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            year = form.cleaned_data['year']
            director = form.cleaned_data['director']
            Movie.objects.create(title=title, year=year, director=director)
            return redirect('/')
        return render(request, 'form.html', {'form': form})


class AddStudioView(View):

    def get(self, request):
        form = StudioAddForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = StudioAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'form.html', {'form': form})


class MovieDetailView(View):

    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        form = CommentAddForm()
        return render(request, 'movie_detail.html', {'movie': movie, 'form': form})


class AddCommentView(LoginRequiredMixin, View):

    def post(self, request, movie_pk):
        form = CommentAddForm(request.POST)
        movie = Movie.objects.get(pk=movie_pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.author = request.user
            comment.save()
            return redirect('detail_movie', movie_pk)

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ""
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            message = "nie poprawne hasło lub/i nazwa użytkownika"
        return render(request, 'form.html', {'form': form, 'message':message})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):

    def get(self, request):
        form = UserCreateForm()
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.set_password(form.cleaned_data['password'])
            u.save()
            return redirect("index")
        return render(request, 'form.html', {'form':form})