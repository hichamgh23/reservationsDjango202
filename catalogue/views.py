"""
views.py — Contrôleurs de l'application catalogue

Organisation :
    1.  Accueil (citation externe)
    2.  Authentification (inscription, déconnexion, mot de passe)
    3.  Profil utilisateur (photo, suppression)
    4.  Spectacles (liste, détail)
    5.  Réservations (création, annulation, export CSV)
    6.  Artistes — CRUD complet
    7.  Lieux (locations) — lecture seule
    8.  Localités — CRUD complet
    9.  Flux RSS
"""

import csv
import requests

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.syndication.views import Feed
from django.db.models import Min, Max, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import SignUpForm, ArtistForm, LocalityForm, ReviewForm
from .models import (
    Artist, ArtistType, ArtistTypeShow, Location, Locality,
    Profile, Representation, Reservation, Show,
)


# ─────────────────────────────────────────────
# UTILITAIRE : restriction par groupe
# ─────────────────────────────────────────────

def group_required(*group_names):
    """Décorateur : accès réservé aux membres des groupes spécifiés (ou superuser)."""
    def in_groups(user):
        if user.is_authenticated:
            if user.groups.filter(name__in=group_names).exists() or user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


# ─────────────────────────────────────────────
# 1. ACCUEIL
# ─────────────────────────────────────────────

def welcome(request):
    """Page d'accueil avec citation aléatoire via l'API DummyJSON."""
    citation = None
    auteur = None
    try:
        response = requests.get('https://dummyjson.com/quotes/random', timeout=3, verify=False)
        if response.status_code == 200:
            data = response.json()
            citation = data.get('quote')
            auteur = data.get('author')
    except Exception:
        pass  # Échec silencieux : la page s'affiche sans citation

    return render(request, 'catalogue/welcome.html', {
        'citation': citation,
        'auteur': auteur,
    })


# ─────────────────────────────────────────────
# 2. AUTHENTIFICATION
# ─────────────────────────────────────────────

def signup(request):
    """Inscription : crée l'utilisateur et l'ajoute au groupe MEMBER."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Group.objects.get(name='MEMBER').user_set.add(user)
            messages.success(request, "Inscription réussie !")
            return redirect('login')
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_user(request):
    """Déconnexion et redirection vers l'accueil."""
    auth_logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('welcome')


@login_required
def change_password(request):
    """Modification du mot de passe (maintient la session active après changement)."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Évite la déconnexion automatique
            messages.success(request, 'Mot de passe mis à jour !')
            return redirect('catalogue:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'catalogue/change_password.html', {'form': form})


# ─────────────────────────────────────────────
# 3. PROFIL UTILISATEUR
# ─────────────────────────────────────────────

@login_required
def profile(request):
    """Page profil : liste des réservations de l'utilisateur connecté."""
    reservations = (
        Reservation.objects
        .filter(user=request.user)
        .select_related('representation__show')
        .order_by('-id')
    )
    return render(request, 'catalogue/profile.html', {'reservations': reservations})


@login_required
def profile_update(request):
    """Mise à jour de la photo de profil."""
    if request.method == 'POST' and request.FILES.get('image'):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.image = request.FILES['image']
        profile.save()
        messages.success(request, 'Photo de profil mise à jour !')
    return redirect('catalogue:profile')


@login_required
def delete_profile_image(request):
    """Suppression de la photo de profil (retour à l'image par défaut)."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.image = 'default.jpg'
    profile.save()
    messages.success(request, 'Photo de profil supprimée.')
    return redirect('catalogue:profile')


# ─────────────────────────────────────────────
# 4. SPECTACLES
# ─────────────────────────────────────────────

def show_index(request):
    """Catalogue des spectacles, avec recherche par titre."""
    search = request.GET.get('search', '')
    shows = (
        Show.objects
        .annotate(
            date_debut=Min('representations__when'),
            date_fin=Max('representations__when'),
        )
        .prefetch_related(
            'artisttypeshow_set__artist_type__artist',
            'artisttypeshow_set__artist_type__type',
        )
        .order_by('title')
    )

    if search:
        shows = shows.filter(title__icontains=search)

    return render(request, 'catalogue/show_index.html', {
        'shows': shows,
        'search': search,
    })


def show_detail(request, show_id):
    """Détail d'un spectacle : description, distribution, avis, formulaire de réservation."""
    show = get_object_or_404(Show, id=show_id)
    representations = show.representations.all().order_by('when')
    artistes_show = (
        ArtistTypeShow.objects
        .filter(show=show)
        .select_related('artist_type__artist', 'artist_type__type')
    )
    reviews = show.reviews.filter(validated=True).order_by('-created_at')
    review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.show = show
            new_review.validated = False  # L'avis doit être validé par un admin
            new_review.save()
            messages.success(request, "Merci ! Votre avis sera publié après validation.")
            return redirect('catalogue:show_detail', show_id=show.id)

    return render(request, 'catalogue/show_detail.html', {
        'show': show,
        'representations': representations,
        'artistes_show': artistes_show,
        'reviews': reviews,
        'review_form': review_form,
    })


# ─────────────────────────────────────────────
# 5. RÉSERVATIONS
# ─────────────────────────────────────────────

@login_required
def book_representation(request, representation_id):
    """Réservation d'une représentation : vérifie les places restantes avant création."""
    representation = get_object_or_404(Representation, id=representation_id)
    admin_fees = Decimal('2.00')

    reserved = (
        Reservation.objects
        .filter(representation=representation)
        .aggregate(Sum('places'))['places__sum'] or 0
    )
    capacity = representation.location.capacity if representation.location else 0
    remaining = max(0, capacity - reserved)

    if request.method == 'POST':
        try:
            places = int(request.POST.get('places', 1))
            if places > remaining or places < 1:
                messages.error(request, f"Erreur : {remaining} places restantes.")
                return redirect('catalogue:show_detail', show_id=representation.show.id)

            Reservation.objects.create(
                user=request.user,
                representation=representation,
                places=places,
            )
            total_places = representation.show.price * places
            return render(request, 'catalogue/reservation_confirm.html', {
                'representation': representation,
                'places': places,
                'total_places': total_places,
                'admin_fees': admin_fees,
                'total_final': total_places + admin_fees,
            })
        except ValueError:
            return redirect('catalogue:show_detail', show_id=representation.show.id)

    return render(request, 'catalogue/book.html', {
        'representation': representation,
        'remaining_seats': remaining,
    })


@login_required
def reservation_delete(request, reservation_id):
    """Annulation d'une réservation (uniquement par son propriétaire)."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Réservation annulée avec succès.")
    return redirect('catalogue:profile')


@login_required
@group_required('ADMIN')
def export_reservations_csv(request):
    """Export CSV de toutes les réservations (admin uniquement)."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reservations.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'ID', 'Utilisateur', 'Email', 'Spectacle',
        'Date représentation', 'Lieu', 'Places', 'Prix unitaire', 'Total',
    ])

    reservations = Reservation.objects.select_related(
        'user', 'representation__show', 'representation__location'
    ).all()

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
            total,
        ])

    return response


# ─────────────────────────────────────────────
# 6. ARTISTES — CRUD
# ─────────────────────────────────────────────

def artist_index(request):
    """Liste de tous les artistes triés par nom."""
    artists = Artist.objects.all().order_by('lastname')
    return render(request, 'catalogue/artist_index.html', {'artists': artists})


def artist_show(request, id):
    """Détail d'un artiste avec ses types (fonctions)."""
    artist = get_object_or_404(Artist, id=id)
    artist_types = ArtistType.objects.filter(artist=artist).select_related('type')
    return render(request, 'catalogue/artist_show.html', {
        'artist': artist,
        'artist_types': artist_types,
    })


@login_required
@group_required('ADMIN')
def artist_create(request):
    """Création d'un artiste (admin uniquement)."""
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
        'artist': None,
    })


@login_required
@group_required('ADMIN')
def artist_edit(request, id):
    """Modification d'un artiste existant (admin uniquement)."""
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
        'artist': artist,
    })


@login_required
@group_required('ADMIN')
def artist_delete(request, id):
    """Suppression d'un artiste après confirmation (admin uniquement)."""
    artist = get_object_or_404(Artist, id=id)
    if request.method == 'POST':
        artist.delete()
        messages.success(request, "Artiste supprimé avec succès !")
        return redirect('catalogue:artist_index')
    return render(request, 'catalogue/artist_confirm_delete.html', {'artist': artist})


# ─────────────────────────────────────────────
# 7. LIEUX (LOCATIONS) — Lecture seule
# ─────────────────────────────────────────────

def location_index(request):
    """Liste de tous les lieux triés par nom."""
    locations = Location.objects.all().select_related('locality').order_by('designation')
    return render(request, 'catalogue/location_index.html', {'locations': locations})


def location_show(request, location_id):
    """Détail d'un lieu avec les spectacles associés."""
    location = get_object_or_404(Location, id=location_id)
    shows = Show.objects.filter(location=location)
    return render(request, 'catalogue/location_show.html', {
        'location': location,
        'shows': shows,
    })


# ─────────────────────────────────────────────
# 8. LOCALITÉS — CRUD
# ─────────────────────────────────────────────

def locality_index(request):
    """Liste de toutes les localités triées par nom."""
    localities = Locality.objects.all().order_by('locality')
    return render(request, 'catalogue/locality_index.html', {'localities': localities})


def locality_show(request, id):
    """Détail d'une localité avec ses lieux associés."""
    locality = get_object_or_404(Locality, id=id)
    locations = locality.locations.all()
    return render(request, 'catalogue/locality_show.html', {
        'locality': locality,
        'locations': locations,
    })


@login_required
@group_required('ADMIN')
def locality_create(request):
    """Création d'une localité (admin uniquement)."""
    form = LocalityForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Localité ajoutée avec succès !")
            return redirect('catalogue:locality_index')
        else:
            messages.error(request, "Échec de l'ajout !")
    return render(request, 'catalogue/locality_form.html', {
        'form': form,
        'action': 'Ajouter',
        'locality': None,
    })


@login_required
@group_required('ADMIN')
def locality_edit(request, id):
    """Modification d'une localité existante (admin uniquement)."""
    locality = get_object_or_404(Locality, id=id)
    form = LocalityForm(request.POST or None, instance=locality)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Localité modifiée avec succès !")
            return redirect('catalogue:locality_show', id=locality.id)
        else:
            messages.error(request, "Échec de la modification !")
    return render(request, 'catalogue/locality_form.html', {
        'form': form,
        'action': 'Modifier',
        'locality': locality,
    })


@login_required
@group_required('ADMIN')
def locality_delete(request, id):
    """Suppression d'une localité après confirmation (admin uniquement)."""
    locality = get_object_or_404(Locality, id=id)
    if request.method == 'POST':
        locality.delete()
        messages.success(request, "Localité supprimée avec succès !")
        return redirect('catalogue:locality_index')
    return render(request, 'catalogue/locality_confirm_delete.html', {'locality': locality})


# ─────────────────────────────────────────────
# 9. FLUX RSS
# ─────────────────────────────────────────────

class LatestRepresentationsFeed(Feed):
    """Flux RSS des 20 prochaines représentations à venir."""
    title = "PickShow — Représentations à venir"
    link = "/shows/"
    description = "Les prochaines représentations programmées sur PickShow"

    def items(self):
        return Representation.objects.filter(when__gte=timezone.now()).order_by('when')[:20]

    def item_title(self, item):
        return item.show.title

    def item_description(self, item):
        lieu = item.location.designation if item.location else 'Lieu non défini'
        return f"Le {item.when.strftime('%d/%m/%Y à %H:%M')} — {lieu}"

    def item_link(self, item):
        return reverse('catalogue:show_detail', args=[item.show.id])
