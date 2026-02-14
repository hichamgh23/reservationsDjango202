from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout as auth_logout # Ajout logout
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum
from .models import Artist, Type, Locality, Role, Location, Show, Representation, Reservation, Profile

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

# 4. Détail du spectacle
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

# 5. Réservation sécurisée
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

# 6. Profil & Historique
@login_required
def profile(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('representation__show').order_by('-id')
    return render(request, 'catalogue/profile.html', {'reservations': reservations})

# 7. Annulation d'une réservation
@login_required
def reservation_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Votre réservation a été annulée avec succès.")
    return redirect('catalogue:profile')

# 8. LA SOLUTION POUR JAZZMIN : Fonction de déconnexion forcée
def logout_user(request):
    auth_logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('welcome')

# 9. Changer le mot de passe
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour !')
            return redirect('catalogue:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'catalogue/change_password.html', {'form': form})

# 10. Mettre à jour la photo de profil
@login_required
def profile_update(request):
    if request.method == 'POST' and request.FILES.get('image'):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.image = request.FILES['image']
        profile.save()
        messages.success(request, 'Photo de profil mise à jour !')
    return redirect('catalogue:profile')

# 11. Supprimer la photo de profil
@login_required
def delete_profile_image(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.image = 'default.jpg'
    profile.save()
    messages.success(request, 'Photo de profil supprimée.')
    return redirect('catalogue:profile')