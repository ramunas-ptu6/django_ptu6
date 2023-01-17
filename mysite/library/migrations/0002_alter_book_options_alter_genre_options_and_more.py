# Generated by Django 4.1.1 on 2023-01-17 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"verbose_name": "Knyga", "verbose_name_plural": "Knygos"},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"verbose_name": "Žanras", "verbose_name_plural": "Žanrai"},
        ),
        migrations.AddField(
            model_name="author",
            name="description",
            field=models.TextField(
                default="bio", max_length=2000, verbose_name="Aprašymas"
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books",
                to="library.author",
            ),
        ),
    ]
