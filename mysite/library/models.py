from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Įveskite knygos žanrą')

    def __str__(self):
        return self.name
