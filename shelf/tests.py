import pytest
from django.test import Client
from django.urls import reverse

from shelf.forms import CommentAddForm, StudioAddForm
from shelf.models import Person, Studio, Comment


def test_index_view():
    client = Client()  # otwieramy przegladarke
    url = reverse('index')  # mowimy na jaki url chcemy wejsc
    response = client.get(url)  # wchodzimy na url
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_person(persons):
    client = Client()
    url = reverse('list_person')
    response = client.get(url)
    persons_context = response.context['persons']
    assert persons_context.count() == len(persons)
    for p in persons:
        assert p in persons_context


@pytest.mark.django_db
def test_list_movies(movies):
    client = Client()
    url = reverse('list_movie')
    response = client.get(url)
    movie_context = response.context['movies']
    assert movie_context.count() == len(movies)
    for m in movies:
        assert m in movie_context


@pytest.mark.django_db
def test_list_person(movie):
    client = Client()
    url = reverse('detail_movie', args=(movie.id,))
    response = client.get(url)
    assert movie == response.context['movie']
    form = response.context['form']
    assert isinstance(form, CommentAddForm)


@pytest.mark.django_db
def test_create_person():
    client = Client()
    url = reverse('create_person')
    response = client.get(url)
    assert 200 == response.status_code


@pytest.mark.django_db
def test_create_person_post():
    data = {
        'first_name': 'test',
        'last_name': 'testowy'
    }
    client = Client()
    url = reverse('create_person')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Person.objects.get(first_name='test', last_name='testowy')


@pytest.mark.django_db
def test_add_studio_get():
    client = Client()
    url = reverse('add_stuido')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], StudioAddForm)

@pytest.mark.django_db
def test_add_studio_post_valid():
    client = Client()
    url = reverse('add_stuido')
    data = {
        'name':'Bambus',
        'year': 1999
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Studio.objects.get(**data)
    #assert Studio.objects.get(name='Bambus',year=1999)

@pytest.mark.django_db
def test_add_studio_post_valid():
    client = Client()
    url = reverse('add_stuido')
    data = {
        'name':'Bambus',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Studio.objects.count()==0
    assert isinstance(response.context['form'], StudioAddForm)


@pytest.mark.django_db
def test_add_comment_to_movie_without_permission(user, movie):
    client = Client()
    url = reverse('add_comment', args=(movie.id,))
    client.force_login(user)
    data = {
        'text':'Ale nudy usypiam'
    }
    response = client.post(url, data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_add_comment_to_movie(user_with_permission, movie):
    client = Client()
    url = reverse('add_comment', args=(movie.id,))
    client.force_login(user_with_permission)
    data = {
        'text':'Ale nudy usypiam'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Comment.objects.get(author=user_with_permission, **data)