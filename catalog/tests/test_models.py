from django.test import TestCase
from catalog.models import Autor

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Autor.objects.create(nombre='Big', apellido='Bob')

    def test_first_name_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('nombre').verbose_name
        self.assertEqual(field_label, 'nombre')

    def test_last_name_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('apellido').verbose_name
        self.assertEqual(field_label, 'apellido')

    def test_date_of_birth_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('nacimiento').verbose_name
        self.assertEqual(field_label, 'nacimiento')

    def test_date_of_death_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('muerte').verbose_name
        self.assertEqual(field_label, 'Muerte')

    def test_first_name_max_length(self):
        autor = Autor.objects.get(id=1)
        max_length = autor._meta.get_field('nombre').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        autor = Autor.objects.get(id=1)
        max_length = autor._meta.get_field('apellido').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        autor = Autor.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(autor.apellido, autor.nombre)

        self.assertEqual(str(autor), expected_object_name)

    def test_get_absolute_url(self):
        autor = Autor.objects.get(id=1)
        self.assertEqual(autor.get_absolute_url(), '/catalog/autor/1')