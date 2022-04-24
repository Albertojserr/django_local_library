from django.contrib import admin
from .models import Autor, Genero, Libro, BookInstance

#admin.site.register(Libro)
#admin.site.register(Autor)
admin.site.register(Genero)
#admin.site.register(BookInstance)
class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Libro
    extra=0

# Define the admin class
class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'nacimiento', 'muerte')
    fields = ['nombre', 'apellido', ('nacimiento', 'muerte')]
    inlines = [BooksInline]
# Register the admin class with the associated model
admin.site.register(Autor, AutorAdmin)
# Register the Admin classes for Book using the decorator

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'mostrar_genero')
    inlines = [BooksInstanceInline]
# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=('libro','status', 'borrower', 'due_back','id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('libro', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
