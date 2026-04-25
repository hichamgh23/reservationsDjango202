from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout as auth_logout
from django.contrib.auth.models import Group
from django.contrib import messages
from decimal import Decimal
from django.db.models import Min, Max, Sum
from .models import Artist, Type, Locality, Role, Location, Show, Representation, Reservation, Profile, ArtistType
from .forms import SignUpForm, ArtistForm
import csv
from django.http import HttpResponse
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone

# Vérification du groupe
def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            if user.groups.filter(name__in=group_names).exists() or user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

# 1. Accueil
import requests

def welcome(request):
    citation = None
    auteur = None
    try:
        response = requests.get('https://dummyjson.com/quotes/random', timeout=3, verify=False)
        if response.status_code == 200:
            data = response.json()
            citation = data.get('quote')
            auteur = data.get('author')
    except Exception:
        pass
    
    return render(request, 'catalogue/welcome.html', {
        'citation': citation,
        'auteur': auteur
    })

# 2. Inscription
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            memberGroup = Group.objects.get(name='MEMBER')
            memberGroup.user_set.add(user)
            messages.success(request, "Inscription réussie !")
            return redirect('login')
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# 3. Catalogue des spectacles
def show_index(request):
    search = request.GET.get('search', '')
    shows = Show.objects.annotate(
        date_debut=Min('representations__when'),
        date_fin=Max('representations__when')
    ).order_by('title')
    
    if search:
        shows = shows.filter(title__icontains=search)
    
    return render(request, 'catalogue/show_index.html', {
        'shows': shows,
        'search': search
    })

# 4. Détail d'un spectacle
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    representations = show.representations.all().order_by('when')
    return render(request, 'catalogue/show_detail.html', {
        'show': show,
        'representations': representations
    })

# 5. Réservation
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

    return render(request, 'catalogue/book.html', {
        'representation': representation,
        'remaining_seats': remaining
    })

# 6. Profil
@login_required
def profile(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('representation__show').order_by('-id')
    return render(request, 'catalogue/profile.html', {'reservations': reservations})

# 7. Annulation réservation
@login_required
def reservation_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Réservation annulée avec succès.")
    return redirect('catalogue:profile')

# 8. Déconnexion
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
            messages.success(request, 'Mot de passe mis à jour !')
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

# --- CRUD ARTIST ---

def artist_index(request):
    artists = Artist.objects.all().order_by('lastname')
    return render(request, 'catalogue/artist_index.html', {'artists': artists})

def artist_show(request, id):
    artist = get_object_or_404(Artist, id=id)
    artist_types = ArtistType.objects.filter(artist=artist).select_related('type')
    return render(request, 'catalogue/artist_show.html', {
        'artist': artist,
        'artist_types': artist_types
    })

@login_required
@group_required('ADMIN')
def artist_create(request):
    form = ArtistForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Artiste ajouté avec succès !")
            return redirect('catalogue:artist_index')
        else:
            messages.error(request, "Échec de l'ajout !")
    return render(request, 'catalogue/artist_form.html', {
        'form': form,
        'action': 'Ajouter',
        'artist': None
    })

@login_required
@group_required('ADMIN')
def artist_edit(request, id):
    artist = get_object_or_404(Artist, id=id)
    form = ArtistForm(request.POST or None, instance=artist)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Artiste modifié avec succès !")
            return redirect('catalogue:artist_show', id=artist.id)
        else:
            messages.error(request, "Échec de la modification !")
    return render(request, 'catalogue/artist_form.html', {
        'form': form,
        'action': 'Modifier',
        'artist': artist
    })

@login_required
@group_required('ADMIN')
def artist_delete(request, id):
    artist = get_object_or_404(Artist, id=id)
    if request.method == 'POST':
        artist.delete()
        messages.success(request, "Artiste supprimé avec succès !")
        return redirect('catalogue:artist_index')
    return render(request, 'catalogue/artist_confirm_delete.html', {'artist': artist})



# --- EXPORT CSV ---
@login_required
@group_required('ADMIN')
def export_reservations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reservations.csv"'
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Utilisateur', 'Email', 'Spectacle', 'Date représentation', 'Lieu', 'Places', 'Prix unitaire', 'Total'])
    
    reservations = Reservation.objects.select_related('user', 'representation__show', 'representation__location').all()
    
    for res in reservations:
        total = res.places * res.representation.show.price + Decimal('2.00')
        writer.writerow([
            res.id,
            res.user.username,
            res.user.email,
            res.representation.show.title,
            res.representation.when.strftime('%d/%m/%Y %H:%M'),
            res.representation.location.designation if res.representation.location else '-',
            res.places,
            res.representation.show.price,
            total
        ])
    
    return response

# --- LOCATIONS ---
def location_index(request):
    locations = Location.objects.all().select_related('locality').order_by('designation')
    return render(request, 'catalogue/location_index.html', {'locations': locations})

def location_show(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    shows = Show.objects.filter(location=location)
    return render(request, 'catalogue/location_show.html', {
        'location': location,
        'shows': shows
    })

# --- LOCALITIES ---
def locality_index(request):
    localities = Locality.objects.all().order_by('locality')
    return render(request, 'catalogue/locality_index.html', {'localities': localities})


# --- FLUX RSS ---
class LatestRepresentationsFeed(Feed):
    title = "PickShow - Représentations à venir"
    link = "/shows/"
    description = "Les prochaines représentations programmées sur PickShow"

    def items(self):
        return Representation.objects.filter(when__gte=timezone.now()).order_by('when')[:20]

    def item_title(self, item):
        return item.show.title

    def item_description(self, item):
        lieu = item.location.designation if item.location else 'Lieu non défini'
        return f"Le {item.when.strftime('%d/%m/%Y à %H:%M')} - {lieu}"

    def item_link(self, item):
        return reverse('catalogue:show_detail', args=[item.show.id])