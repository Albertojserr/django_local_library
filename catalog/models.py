from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from datetime import date
class Genero(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.nombre

class Libro(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genero = models.ManyToManyField(Genero, help_text="Seleccione un genero para este libro")
    def mostrar_genero(self):
        return ', '.join([ genero.nombre for genero in self.genero.all()[:3] ])
    mostrar_genero.short_description = 'Genero'
    def __str__(self):
        return self.titulo


    def get_absolute_url(self):
        return reverse('libro-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return f'{self.id} ({self.libro.titulo})'

class Autor(models.Model):
    """
    Modelo que representa un autor
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacimiento = models.DateField(null=True, blank=True)
    muerte = models.DateField('Muerte', null=True, blank=True)
    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('autor-detail', args=[str(self.id)])
    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.apellido, self.nombre)
    class Meta:
        ordering = ['apellido']

@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False