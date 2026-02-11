from django.db import models

# 1. Les Localités (Villes)
class Locality(models.Model):
    postal_code = models.CharField(max_length=6)
    locality = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.postal_code} {self.locality}"

    class Meta:
        db_table = "localities"

# 2. Les Lieux (Salles de spectacle)
class Location(models.Model):
    slug = models.SlugField(max_length=60, unique=True)
    designation = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, related_name='locations')
    website = models.URLField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.designation

    class Meta:
        db_table = "locations"

# 3. Les Artistes
class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        db_table = "artists"

# 4. Les Types de métiers (Chanteur, Acteur...)
class Type(models.Model):
    type = models.CharField(max_length=60)

    def __str__(self):
        return self.type

    class Meta:
        db_table = "types"

# 5. Les Rôles (Auteur, Scénographe...)
class Role(models.Model):
    role = models.CharField(max_length=30)

    def __str__(self):
        return self.role

    class Meta:
        db_table = "roles"

# 6. Les Spectacles (Shows)
class Show(models.Model):
    slug = models.SlugField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    poster_url = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shows')
    bookable = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shows"
