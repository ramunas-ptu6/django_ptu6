from django.contrib import admin

from .models import Author, Genre, Book, BookInstance


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    readonly_fields = ('id',)
    can_delete = False
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    search_fields = ('id', 'book__title')
    list_editable = ('due_back', 'status')

    fieldsets = (
        ('General', {'fields': ('id', 'book',)}),
        ('Availability', {'fields': ('status', 'due_back')})
    )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_books')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
