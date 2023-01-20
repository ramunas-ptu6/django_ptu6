from django.contrib import admin

from .models import Author, Genre, Book, BookInstance


class BooksInstanceInline(admin.TabularInline):
    """knygų egzempliorių vaizdavimo klasė
    (sukuria eilutes kurias galima įdėti į kitą viewsą)"""
    model = BookInstance  # modelis iš kurio kuriamos eilutės(turi būti vaikinis kitam modeliui)
    # readonly_fields = ('id',)  # nurodom kad id lauko šiam viewse negalima redaguoti
    # can_delete = False  # negalima trinti
    extra = 0  # kad nepridėtų į viewsą tuščių eilučių


# VISOS iš admin.ModelAdmin paveldinčios klasės keičia standartinį modelio viewsą admin svetainėje
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'get_authname')  # nurodom kokius stulpelius vaizduosime BookInstance
    # viewse admin svetainėje
    # display_genre atsiranda iš metodo aprašyto Book modelyje,
    # models.py faile
    search_fields = ('author__last_name',)
    def get_authname(self, obj): # BONUS - būdas per foreign key pasiekti konkretų lauką tėvinėj lentelėj
        return obj.author.first_name
    get_authname.short_description = 'Autoriaus vardas'
    inlines = [BooksInstanceInline]  # prijungiam papildomą vaizdą(eilutes) iš class BooksInstanceInline


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'reader')  # stulpeliai BookInstance viewse admin svetainėje
    list_filter = ('status', 'due_back')  # sukuriamas filtro skydelis
    search_fields = ('id', 'book__title')  # paieškos laukas
    list_editable = ('due_back', 'status', 'reader')  # nurodom kad į list_display įtraukti stulpeliai gali būti redaguojami

    fieldsets = (  # sukuria atskirus tabus laukams (šie laukai rodomi defaultu, čia sukuriamas tik padalinimas)
        ('General', {'fields': ('id', 'book',)}),  # General, Availability - mūsų sukurti tabų pavadinimai, žodynuose
        ('Availability', {'fields': ('status', 'due_back', 'reader')})  # raktuose fields nurodoma kokie laukai bus kokiam tabe
    )


class AuthorAdmin(admin.ModelAdmin):  # stulpeliai Author viewse admin svetainėje
    list_display = ('last_name', 'first_name', 'display_books')


# !!! kad nūtų naudojami mūsų sukurti admin viewsai, viewsų klases reikia surišti su modelių klasėmis
# panaudojus admin.site.register metodą
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
