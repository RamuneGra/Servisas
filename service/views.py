from .models import AutomobilioModelis, Paslauga, Automobilis, Uzsakymas, UzsakymoEilute, UzsakymuAtsiliepimai
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import UzsakymuAtsiliepimaiForm, UserUpdateForm, ProfilisUpdateForm, VartotojoUzsakymuCreateForm
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _


def index(request):
    num_auto = Automobilis.objects.count()
    num_paslaugos = Paslauga.objects.count()
    num_uzsakymai = Uzsakymas.objects.filter(status__exact='i').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_auto': num_auto,
        'num_paslaugos': num_paslaugos,
        'num_uzsakymai': num_uzsakymai,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)

def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), 8)
    page_number = request.GET.get('page')
    paged_automobiliai = paginator.get_page(page_number)
    context = {
        'automobiliai': paged_automobiliai
    }
    print(automobiliai)
    return render(request, 'automobiliai.html', context=context)

def automobilis(request, automobilis_id):
    vienas_automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'automobilis.html', {'automobilis': vienas_automobilis})

def paslaugos(request):
    paginator = Paginator(Paslauga.objects.all(), 10)
    page_number = request.GET.get('page')
    paged_paslaugos = paginator.get_page(page_number)
    context = {
        'paslaugos': paged_paslaugos
    }
    print(paslaugos)
    return render(request, 'paslaugos.html', context=context)


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 5
    template_name = 'uzsakymas_list.html'


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    form_class = UzsakymuAtsiliepimaiForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('uzsakymas-detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.komentatorius = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(klientas__icontains=query)
                                                | Q(automobilio_modelis__marke__icontains=query)
                                                | Q(automobilio_modelis__modelis__icontains=query)
                                                | Q(valstybinis_nr__icontains=query)
                                                | Q(vin_kodas__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})


class CustomLogout(LogoutView):
    template_name = 'registration/logged_out.html'


class VartotojoUzsakymuListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'user_order.html'
    paginate_by = 5

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user).filter(status__exact='v').order_by('terminas')


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %s already exists!') % username)
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Email %s already exists!') % email)
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, _('Username %s is registered!') % username)
                    return redirect('login')
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('Profile updated'))
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)


class VartotojoUzsakymuCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    # fields = ['automobilis', 'terminas', 'status']
    success_url = "/service/myorders/"
    template_name = 'user_order_form.html'
    form_class = VartotojoUzsakymuCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)


class VartotojoUzsakymuUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    # fields = ['automobilis', 'terminas', 'status']
    success_url = "/service/myorders/"
    template_name = 'user_order_form.html'
    form_class = VartotojoUzsakymuCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class UzsakymoUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas

    success_url = "/service/uzsakymai/<uzsakymas.id>"
    template_name = 'user_order_form.html'
    form_class = VartotojoUzsakymuCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class VartotojoUzsakymuDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/service/myorders/"
    template_name = "user_order_delete.html"

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class UzsakymoDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/service/uzsakymai/"
    template_name = "order_delete.html"

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class VartotojoEilutesCreateView(LoginRequiredMixin, generic.CreateView):
    model = UzsakymoEilute
    fields = ['paslauga', 'kiekis']
    template_name = 'uzsakymoeilute_form.html'

    def get_success_url(self):
        return reverse("uzsakymas-detail", kwargs={"pk": self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        return self.request.user == uzsakymas.vartotojas


class VartotojoEilutesUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = UzsakymoEilute
    fields = ['paslauga', 'kiekis']
    template_name = 'uzsakymoeilute_form.html'

    def get_success_url(self):
        return reverse("uzsakymas-detail", kwargs={"pk": self.kwargs['uzsakymai_pk']})

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymai_pk'])
        form.save()
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymai_pk'])
        return self.request.user == uzsakymas.vartotojas


class VartotojoEilutesDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = UzsakymoEilute
    template_name = "uzsakymoeilute_delete.html"

    def get_success_url(self):
        return reverse("uzsakymas-detail", kwargs={"pk": self.kwargs['uzsakymai_pk']})

    def test_func(self):
        uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymai_pk'])
        return self.request.user == uzsakymas.vartotojas