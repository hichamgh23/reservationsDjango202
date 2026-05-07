"""
models.py — Modèles de base de données de l'application catalogue

Schéma relationnel :
    Artist ──< ArtistType >── Type
    ArtistType ──< ArtistTypeShow >── Show
    Show ──< Representation >── Location ──> Locality
    Representation ──< Reservation >── User
    User ──── Profile (OneToOne)
    User ──── UserMeta (OneToOne)
    Show ──< Review >── User
"""

from django.db import models
from django.contrib.auth.models import User


# ─────────────────────────────────────────────
# ENTITÉS DE BASE
# ─────────────────────────────────────────────

class Artist(models.Model):
    """Artiste ou interprète référencé dans le système."""
    firstname = models.CharField(max_length=60)
    lastname  = models.CharField(max_length=60)

    class Meta:
        db_table = "artists"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Type(models.Model):
    """Type de spectacle ou de prestation (ex : théâtre, danse…)."""
    type = models.CharField(max_length=60)

    class Meta:
        db_table = "types"

    def __str__(self):
        return self.type


class Locality(models.Model):
    """Commune ou code postal (ex : 1000 Bruxelles)."""
    postal_code = models.CharField(max_length=6)
    locality    = models.CharField(max_length=60)

    class Meta:
        db_table = "localities"

    def __str__(self):
        return f"{self.postal_code} {self.locality}"


class Role(models.Model):
    """Rôle joué par un artiste dans un spectacle (ex : acteur, metteur en scène)."""
    role = models.CharField(max_length=30)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.role


# ─────────────────────────────────────────────
# LIEUX & SPECTACLES
# ─────────────────────────────────────────────

class Location(models.Model):
    """Salle ou lieu de représentation."""
    slug        = models.SlugField(max_length=60, unique=True)
    designation = models.CharField(max_length=60)
    address     = models.CharField(max_length=255)
    locality    = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True,
                                    related_name='locations')
    website     = models.URLField(max_length=255, null=True, blank=True)
    phone       = models.CharField(max_length=30, null=True, blank=True)
    capacity    = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "locations"

    def __str__(self):
        return self.designation


class Show(models.Model):
    """Spectacle affiché dans le catalogue."""
    slug        = models.SlugField(max_length=60, unique=True)
    title       = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    poster_url  = models.CharField(max_length=255, null=True, blank=True)
    location    = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                    related_name='shows')
    bookable    = models.BooleanField(default=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "shows"

    def __str__(self):
        return self.title


class Representation(models.Model):
    """Séance d'un spectacle à une date et un lieu précis."""
    show     = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='representations')
    when     = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                  related_name='representations')

    class Meta:
        db_table = "representations"

    def __str__(self):
        return f"{self.show.title} — {self.when}"


# ─────────────────────────────────────────────
# RELATIONS ARTISTES ↔ SPECTACLES
# ─────────────────────────────────────────────

class ArtistType(models.Model):
    """Association Artiste ↔ Type (une fonction pour un artiste donné)."""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    type   = models.ForeignKey(Type,   on_delete=models.CASCADE)

    class Meta:
        db_table = "artist_type"

    def __str__(self):
        return f"{self.artist} — {self.type.type}"


class ArtistTypeShow(models.Model):
    """Participation d'un ArtistType à un spectacle."""
    artist_type = models.ForeignKey(ArtistType, on_delete=models.CASCADE)
    show        = models.ForeignKey(Show,        on_delete=models.CASCADE)

    class Meta:
        db_table = "artist_type_show"

    def __str__(self):
        return f"{self.artist_type} → {self.show.title}"


# ─────────────────────────────────────────────
# UTILISATEURS
# ─────────────────────────────────────────────

class Reservation(models.Model):
    """Réservation d'un utilisateur pour une représentation."""
    user           = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='reservations')
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE,
                                       related_name='reservations')
    places         = models.PositiveIntegerField()

    class Meta:
        db_table = "reservations"

    def __str__(self):
        return f"Réservation de {self.user.username} — {self.representation.show.title}"


class Profile(models.Model):
    """Extension du modèle User : photo de profil."""
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return f"Profil de {self.user.username}"


class UserMeta(models.Model):
    """Extension du modèle User : préférences (langue)."""
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    langue = models.CharField(max_length=2)

    class Meta:
        db_table = "user_meta"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# ─────────────────────────────────────────────
# AVIS
# ─────────────────────────────────────────────

class Review(models.Model):
    """Avis d'un utilisateur sur un spectacle (nécessite validation admin)."""
    user       = models.ForeignKey(User, on_delete=models.RESTRICT, null=False,
                                   related_name='reviews')
    show       = models.ForeignKey(Show, on_delete=models.RESTRICT, null=False,
                                   related_name='reviews')
    review     = models.TextField()
    stars      = models.PositiveSmallIntegerField()
    validated  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"{self.user.username} — {self.show.title} : {self.stars}★"
