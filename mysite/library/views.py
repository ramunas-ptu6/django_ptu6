from django.shortcuts import render

from .models import Author, Book, BookInstance


def index(request):
    # count užklausos(queries)
    num_books = Book.objects.all().count()  # suskaičiuojam knygas
    num_instances = BookInstance.objects.all().count  # suskaičiuojam knygų kopijas

    # suskaičiuojam laisvas knygas(statusas g)
    num_instances_available = BookInstance.objects.filter(status__exact="g").count()

    # suskaičiuojam autorius
    num_authors = Author.objects.all().count()



    context = {  # šablono konteksto kintamasis
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }

    # formuojam galutinį vaizdą iš šablono index.html ir duomenų
    # context žodyne(request - užklausa atėjusi iš kliento)
    return render(request, 'index.html', context=context)
