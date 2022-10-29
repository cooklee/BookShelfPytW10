from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from shelf.models import Person


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
        return render(request, 'PersonList.html', {'persons':osoby})