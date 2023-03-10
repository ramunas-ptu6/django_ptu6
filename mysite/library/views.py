from django.contrib import messages
from django.contrib.auth.forms import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserBookCreateForm
from .models import Author, Book, BookInstance


def index(request):
    # count užklausos(queries)
    num_books = Book.objects.all().count()  # suskaičiuojam knygas
    num_instances = BookInstance.objects.all().count  # suskaičiuojam knygų kopijas

    # suskaičiuojam laisvas knygas(statusas g)
    num_instances_available = BookInstance.objects.filter(status__exact="g").count()

    # suskaičiuojam autorius
    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {  # šablono konteksto kintamasis
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
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
    paginate_by = 6
    template_name = 'book_list.html'
    # context_object_name = 'my_book_list' galime pasikeisti automatinį konteksto kintamąjį(book_list) į custom pavadinimą
    ordering = ['title']

class BookDetailView(FormMixin, generic.DetailView):
    model = Book  # šablonui autosukuriamas kintamas book
    template_name = 'book_detail_styled.html'
    form_class = BookReviewForm

    class Meta:
        ordering = ['title']

    # nukreipimas po sėkmingo komentaro papostinimo atgal į knygos viewsą
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get("query")
    search_results = Book.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query)
    )

    return render(request, "search.html", {"books": search_results, "query": query})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "user_books.html"

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(status__exact="p").order_by("due_back")


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimam reikšmes iš registracijos formos laukų
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        # ar sutampa įvesti passwordai
        if password1 == password2:
            # ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} užimtas!")
                return redirect("register")
            else:
                # ar nėra tokio pačio email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Emailas {email} jau užimtas kito vartotojo")
                    return redirect("register")
                else:
                    # taškas kai viskas tvarkoje, patikrinimai praeiti, kuriam naują userį
                    User.objects.create_user(username=username, email=email, password=password1)
                    messages.info(request, f"User {username} succesfully registered")
                    return redirect("login")
        else:
            messages.error(request, "Slaptažodžiai nesutampa")
            return redirect("register")
    return render(request, "register.html")


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, "Profilis sėkmingai atnaujintas")
            return redirect("profilis")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, "profilis.html", context=context)


class BookByUserCreateView(LoginRequiredMixin, CreateView):
    model = BookInstance
    # fields = ('book', 'due_back', 'status')
    success_url = '/library/mybooks/'
    template_name = 'user_book_form.html'
    form_class = UserBookCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)


class BookByUserDetailView(LoginRequiredMixin, BookDetailView):
    model = BookInstance
    template_name = 'user_book.html'


class BookByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookInstance
    fields = ('book', 'due_back', 'status')
    success_url = '/library/mybooks/'
    template_name = 'user_book_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bookinstance = self.get_object()
        return self.request.user == bookinstance.reader


class BookByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookInstance
    success_url = '/library/mybooks/'
    template_name = 'user_book_delete.html'

    def test_func(self):
        bookinstance = self.get_object()
        return self.request.user == bookinstance.reader

