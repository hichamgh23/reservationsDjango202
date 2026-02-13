from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum
from .models import Show, Representation, Reservation

# 1. Page d'accueil
def welcome(request):
    return render(request, 'catalogue/welcome.html', {'user': request.user})

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

# 3. Catalogue des spectacles
def show_index(request):
    shows = Show.objects.all().order_by('title')
    return render(request, 'catalogue/show_index.html', {'shows': shows, 'titre': 'Liste des spectacles'})

# 4. Détail du spectacle
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

# 5. Réservation (Logique de stock 100% conforme Source 306)
@login_required
def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    admin_fees = Decimal('2.00')
    
    # Calcul des places déjà réservées
    reserved_seats = Reservation.objects.filter(representation=representation).aggregate(Sum('places'))['places__sum'] or 0
    
    # Capacité totale du lieu
    capacity = representation.location.capacity if representation.location else 0
    
    # Calcul places restantes (on bloque à 0 minimum)
    remaining_seats = max(0, capacity - reserved_seats)

    if request.method == 'POST':
        try:
            places = int(request.POST.get('places', 1))
            
            # Vérification stricte du stock
            if remaining_seats <= 0:
                messages.error(request, "Désolé, cette séance est complète.")
                return redirect('catalogue:show_detail', show_id=representation.show.id)
                
            if places > remaining_seats:
                messages.error(request, f"Désolé, il ne reste que {remaining_seats} places.")
                return redirect('catalogue:show_detail', show_id=representation.show.id)

            if places < 1:
                raise ValueError
            
            # Enregistrement en base de données
            Reservation.objects.create(
                user=request.user, 
                representation=representation, 
                places=places
            )
            
            # Calculs pour la confirmation
            total_places = representation.show.price * places
            total_final = total_places + admin_fees
            
            return render(request, 'catalogue/reservation_confirm.html', {
                'representation': representation,
                'places': places,
                'total_places': total_places,
                'admin_fees': admin_fees,
                'total_final': total_final
            })
        except ValueError:
            messages.error(request, "Veuillez entrer un nombre de places valide.")
            
    return render(request, 'catalogue/book.html', {
        'representation': representation,
        'remaining_seats': remaining_seats
    })