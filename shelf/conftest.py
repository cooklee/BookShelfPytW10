import pytest
from django.contrib.auth.models import User, Permission

from shelf.models import Person, Movie


@pytest.fixture
def persons():
    lst = []
    for n in range(10):
        p = Person.objects.create(first_name=n, last_name=n)
        lst.append(p)
    return lst

@pytest.fixture
def movie(persons):
    person = persons[0]
    return Movie.objects.create(title='Owoc który sie nie kula',
                                year=2022, director=person)

@pytest.fixture
def movies(persons):
    lst = []
    for person in persons:
        m = Movie.objects.create(title="mis", year='1999', director=person)
        lst.append(m)
    return lst

@pytest.fixture
def user():
    u = User.objects.create(username='tadeusz')
    return u

@pytest.fixture
def user_with_permission():
    u = User.objects.create(username='tadeusz')
    permission = Permission.objects.get(codename='add_comment')
    u.user_permissions.add(permission)
    return u