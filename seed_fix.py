"""
seed_fix.py — Correction des liaisons manquantes pour Le Prénom et Le Dîner de Cons
(utilise les slugs et IDs pour éviter les problèmes d'encodage en terminal Windows)
"""
from catalogue.models import Show, Artist, Type, ArtistType, ArtistTypeShow, Review
from django.contrib.auth.models import User

# Récupération par slug (insensible à l'encodage des titres)
le_prenom  = Show.objects.get(slug='le-prenom')
diner_cons = Show.objects.get(slug='le-diner-de-cons')

# Types par ID (vus dans la commande précédente)
comedie  = Type.objects.get(id=2)   # Comédie
theatre  = Type.objects.get(id=3)   # Théâtre
impro    = Type.objects.get(id=8)   # Improvisation

print("=== ArtistTypeShow : Le Prénom ===")
for fname, lname, typ in [
    ('Sophie',   'Deprez',  comedie),
    ('Marc',     'Delcourt', comedie),
    ('Jean-Luc', 'Piraux',  impro),
]:
    a = Artist.objects.get(firstname=fname, lastname=lname)
    at, _ = ArtistType.objects.get_or_create(artist=a, type=typ)
    obj, c = ArtistTypeShow.objects.get_or_create(artist_type=at, show=le_prenom)
    print(f"  {'[+]' if c else '[ ]'} {a} ({typ.type}) -> Le Prénom")

print("\n=== ArtistTypeShow : Le Dîner de Cons ===")
for fname, lname, typ in [
    ('Marc',     'Delcourt', comedie),
    ('Jean-Luc', 'Piraux',  comedie),
    ('Pierre',   'Bodson',  comedie),
]:
    a = Artist.objects.get(firstname=fname, lastname=lname)
    at, _ = ArtistType.objects.get_or_create(artist=a, type=typ)
    obj, c = ArtistTypeShow.objects.get_or_create(artist_type=at, show=diner_cons)
    print(f"  {'[+]' if c else '[ ]'} {a} ({typ.type}) -> Le Dîner de Cons")

print("\n=== Avis manquants ===")
hicham = User.objects.get(username='hicham')
reviews_data = [
    (hicham, le_prenom,  4, "Excellent spectacle, le texte est tres bien ecrit. Les acteurs sont convaincants.", True),
    (hicham, diner_cons, 5, "Un classique incontournable ! On rit du debut a la fin, le timing comique est parfait.", True),
]
for user, show, stars, text, validated in reviews_data:
    exists = Review.objects.filter(user=user, show=show).exists()
    if not exists:
        Review.objects.create(user=user, show=show, stars=stars, review=text, validated=validated)
        print(f"  [+] Avis : {user.username} -> {show.slug} ({stars}*)")
    else:
        print(f"  [ ] Deja existant : {user.username} -> {show.slug}")

print("\n=== TOTAUX FINAUX ===")
print("ArtistTypeShow :", ArtistTypeShow.objects.count())
print("Reviews        :", Review.objects.count())
