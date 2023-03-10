import uuid
from datetime import date

from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


# Create your models here.
class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Įveskite knygos žanrą')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"


class Book(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books')
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Išrinkite žanrą/us šiai knygai')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def display_genre(self):
        return '; '.join([genre.name for genre in self.genre.all()])

    display_genre.short_description = 'Žanras'

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        # ordering = ["title"]
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus knygos kopijos ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Status'
    )

    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']  # admin svetainės settingas, kaip rikiuojama

    def __str__(self):
        return f'{self.id} {self.book.title}'


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    # description = models.TextField('Aprašymas', max_length=2000, default='bio')
    description = HTMLField(default="")

    def display_books(self):
        return ', '.join([book.title for book in self.books.all()][:3]) + "..."

    display_books.short_description = 'Knygos'

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class BookReview(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
