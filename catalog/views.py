from django.shortcuts import render
from .models import Libro, Autor, BookInstance, Genero
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
import datetime
from django.contrib.auth.decorators import permission_required
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def index(request):
    num_libros=Libro.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_autores=Autor.objects.count()
    num_generos=Genero.objects.count()
    num_visitas = request.session.get('num_visitas', 0)
    request.session['num_visitas'] = num_visitas + 1

    context = {
        'num_libros':num_libros,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_autores':num_autores,
        'num_generos':num_generos,
        'num_visitas':num_visitas,
    }
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Libro
    paginate_by = 10
class BookDetailView(generic.DetailView):
    model = Libro
    paginate_by = 10
class AuthorListView(generic.ListView):
    model = Autor
    paginate_by = 10
class AuthorDetailView(generic.DetailView):
    model = Autor
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Autor
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    initial={'muerte':'05/01/2018',}

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Autor
    permission_required = 'catalog.can_mark_returned'
    fields = ['nombre','apellido','nacimiento','muerte']

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Autor
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('autors')

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Libro
    fields = '__all__'
    initial={'muerte':'12/10/2016',}
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Libro
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Libro
    success_url = reverse_lazy('libros')
    permission_required = 'catalog.can_mark_returned'

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


