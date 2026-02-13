from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum
from .models import Show, Representation, Reservation

# 1. Accueil
def welcome(request):
    return render(request, 'catalogue/welcome.html')

# 2. Inscription
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie !")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# 3. Liste des spectacles
def show_index(request):
    shows = Show.objects.all().order_by('title')
    return render(request, 'catalogue/show_index.html', {'shows': shows})

# 4. Détail du spectacle (C'est celle-ci qui manquait dans ton erreur !)
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

# 5. Réservation sécurisée (Source 306)
@login_required
def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    admin_fees = Decimal('2.00')
    
    reserved = Reservation.objects.filter(representation=representation).aggregate(Sum('places'))['places__sum'] or 0
    capacity = representation.location.capacity if representation.location else 0
    remaining = max(0, capacity - reserved)

    if request.method == 'POST':
        try:
            places = int(request.POST.get('places', 1))
            if places > remaining or places < 1:
                messages.error(request, f"Erreur : {remaining} places restantes.")
                return redirect('catalogue:show_detail', show_id=representation.show.id)
            
            Reservation.objects.create(user=request.user, representation=representation, places=places)
            
            total_places = representation.show.price * places
            return render(request, 'catalogue/reservation_confirm.html', {
                'representation': representation,
                'places': places,
                'total_places': total_places,
                'admin_fees': admin_fees,
                'total_final': total_places + admin_fees
            })
        except ValueError:
            return redirect('catalogue:show_detail', show_id=representation.show.id)
            
    return render(request, 'catalogue/book.html', {'representation': representation, 'remaining_seats': remaining})

# 6. Profil & Historique (Source 21 & 40)
@login_required
def profile(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('representation__show').order_by('-id')
    return render(request, 'catalogue/profile.html', {'reservations': reservations})