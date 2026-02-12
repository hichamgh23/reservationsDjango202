from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Show, Representation, Reservation

# 1. Page d'accueil
def welcome(request):
    return render(request, 'catalogue/welcome.html', {'user': request.user})

# 2. Inscription (Scénario nominal Source 36)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Hashage et enregistrement auto [cite: 36]
            messages.success(request, "Inscription réussie !")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# 3. Catalogue des spectacles (Source 180)
def show_index(request):
    shows = Show.objects.all().order_by('title')
    return render(request, 'catalogue/show_index.html', {'shows': shows, 'titre': 'Catalogue'})

# 4. Détail du spectacle (Source 10)
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

# 5. Réservation (Chapitre 10)
@login_required
def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    if request.method == 'POST':
        nb_places = int(request.POST.get('places', 1))
        Reservation.objects.create(user=request.user, representation=representation, places=nb_places) # [cite: 9]
        return render(request, 'catalogue/reservation_confirm.html', {'representation': representation, 'places': nb_places})
    return render(request, 'catalogue/book.html', {'representation': representation})