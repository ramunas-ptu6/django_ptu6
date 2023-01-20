from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic

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


def authors(request):
    # authors = Author.objects.all()
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})


class BookListView(generic.ListView):
    model = Book  # pagal modelio pav. autosukuriamas book_list kintamasis(visi objektai iš klasės) perduodamas į šabloną
    paginate_by = 4
    template_name = 'book_list.html'
    # context_object_name = 'my_book_list' galime pasikeisti automatinį konteksto kintamąjį(book_list) į custom pavadinimą


class BookDetailView(generic.DetailView):
    model = Book  # šablonui autosukuriamas kintamas book
    template_name = 'book_detail_styled.html'


def search(request):
    query = request.GET.get("query")
    search_results = Book.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query)
    )

    return render(request, "search.html", {"books": search_results, "query": query})
