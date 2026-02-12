from django.db import models
from django.contrib.auth.models import User

# 1. Artistes (Source 731)
class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)

    class Meta:
        db_table = "artists"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

# 2. Types (Source 934)
class Type(models.Model):
    type = models.CharField(max_length=60)

    class Meta:
        db_table = "types"

    def __str__(self):
        return self.type

# 3. Localités (Source 934)
class Locality(models.Model):
    postal_code = models.CharField(max_length=6)
    locality = models.CharField(max_length=60)

    class Meta:
        db_table = "localities"

    def __str__(self):
        return f"{self.postal_code} {self.locality}"

# 4. Rôles (Source 934)
class Role(models.Model):
    role = models.CharField(max_length=30)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.role

# 5. Lieux (Locations) (Source 320)
class Location(models.Model):
    slug = models.SlugField(max_length=60, unique=True)
    designation = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, related_name='locations')
    website = models.URLField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = "locations"

    def __str__(self):
        return self.designation

# 6. ArtistType (Relation Artiste-Type)
class ArtistType(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = "artist_type"

    def __str__(self):
        return f"{self.artist.firstname} {self.artist.lastname} - {self.type.type}"

# 7. Spectacles (Shows) (Source 348)
class Show(models.Model):
    slug = models.SlugField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    poster_url = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shows')
    bookable = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "shows"

    def __str__(self):
        return self.title

    def get_authors(self):
        """Récupère les artistes de type 'scénographe' (Source 335, 354)"""
        authors = []
        # On utilise une chaîne de caractères 'ArtistTypeShow' pour éviter l'erreur d'ordre
        for collaboration in ArtistTypeShow.objects.filter(show=self):
            if collaboration.artist_type.type.type.lower() == "scénographe":
                authors.append(collaboration.artist_type.artist)
        return authors

# 8. ArtistTypeShow (Lien final)
class ArtistTypeShow(models.Model):
    artist_type = models.ForeignKey(ArtistType, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    class Meta:
        db_table = "artist_type_show"

    def __str__(self):
        return f"{self.artist_type} - {self.show.title}"

# 9. Représentations (Source 306)
class Representation(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='representations')
    when = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='representations')

    class Meta:
        db_table = "representations"

    def __str__(self):
        return f"{self.show.title} - {self.when}"

# 10. Réservations (Source 8, 9)
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, related_name='reservations')
    places = models.PositiveIntegerField()

    class Meta:
        db_table = "reservations"

    def __str__(self):
        return f"Réservation de {self.user.username}"