"""
seed_data.py — Peuplement réaliste de la base de données PickShow

Contenu : spectacles de théâtre/comédie à Bruxelles (données vraisemblables)

Usage :
    python manage.py shell < seed_data.py
    -- ou --
    python manage.py shell -c "exec(open('seed_data.py').read())"

Le script est idempotent : get_or_create évite les doublons.
"""

import os
import django

# Nécessaire uniquement si exécuté hors du shell Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from catalogue.models import (
    Artist, ArtistType, ArtistTypeShow,
    Location, Locality, Profile,
    Representation, Reservation,
    Review, Role, Show, Type, UserMeta,
)

print("\n" + "="*55)
print("  SEED — PickShow (Bruxelles)")
print("="*55)


# ─────────────────────────────────────────────
# 1. TYPES DE SPECTACLE
# ─────────────────────────────────────────────
print("\n[1/9] Types de spectacle...")

types_data = [
    "Comédie",
    "Théâtre",
    "Drame",
    "One-man-show",
    "Danse",
    "Musique",
    "Improvisation",
]

types_objs = {}
for name in types_data:
    obj, created = Type.objects.get_or_create(type=name)
    types_objs[name] = obj
    print(f"  {'[+]' if created else '[ ]'} Type : {name}")

# Récupérer le type "rire" existant et le mapper
rire = Type.objects.filter(type="rire").first()
if rire:
    types_objs["rire"] = rire

print(f"  Total Types : {Type.objects.count()}")


# ─────────────────────────────────────────────
# 2. RÔLES
# ─────────────────────────────────────────────
print("\n[2/9] Rôles...")

roles_data = [
    "Acteur",
    "Actrice",
    "Metteur en scène",
    "Metteuse en scène",
    "Comédien",
    "Comédienne",
    "Musicien",
]

roles_objs = {}
for name in roles_data:
    obj, created = Role.objects.get_or_create(role=name)
    roles_objs[name] = obj
    print(f"  {'[+]' if created else '[ ]'} Rôle : {name}")

print(f"  Total Roles : {Role.objects.count()}")


# ─────────────────────────────────────────────
# 3. LOCALITÉS BRUXELLOISES
# ─────────────────────────────────────────────
print("\n[3/9] Localités...")

localities_data = [
    ("1050", "Ixelles"),
    ("1060", "Saint-Gilles"),
    ("1080", "Molenbeek-Saint-Jean"),
    ("1030", "Schaerbeek"),
    ("1180", "Uccle"),
    ("1190", "Forest"),
    ("1140", "Evere"),
]

localities_objs = {}
for postal, name in localities_data:
    obj, created = Locality.objects.get_or_create(postal_code=postal, locality=name)
    localities_objs[name] = obj
    print(f"  {'[+]' if created else '[ ]'} {postal} {name}")

# Récupérer les localités existantes
for loc in Locality.objects.all():
    localities_objs[loc.locality] = loc

print(f"  Total Localities : {Locality.objects.count()}")


# ─────────────────────────────────────────────
# 4. LIEUX (LOCATIONS)
# ─────────────────────────────────────────────
print("\n[4/9] Lieux de représentation...")

locations_data = [
    {
        "slug":        "theatre-national-bruxelles",
        "designation": "Théâtre National de Bruxelles",
        "address":     "Boulevard Emile Jacqmain 111-115",
        "locality":    "Bruxelles",
        "website":     "https://www.theatrenational.be",
        "phone":       "+32 2 203 41 55",
        "capacity":    800,
    },
    {
        "slug":        "theatre-les-riches-claires",
        "designation": "Théâtre Les Riches Claires",
        "address":     "Rue des Riches Claires 24",
        "locality":    "Bruxelles",
        "website":     "https://www.lesrichesclaires.be",
        "phone":       "+32 2 548 25 80",
        "capacity":    200,
    },
    {
        "slug":        "theatre-royal-du-parc",
        "designation": "Théâtre Royal du Parc",
        "address":     "Rue de la Loi 3",
        "locality":    "Bruxelles",
        "website":     "https://www.theatreduparc.be",
        "phone":       "+32 2 505 30 30",
        "capacity":    450,
    },
    {
        "slug":        "kaaitheater",
        "designation": "Kaaitheater",
        "address":     "Square Sainctelette 20",
        "locality":    "Bruxelles",
        "website":     "https://www.kaaitheater.be",
        "phone":       "+32 2 201 59 59",
        "capacity":    300,
    },
]

locations_objs = {}
for d in locations_data:
    locality_obj = localities_objs.get(d["locality"])
    obj, created = Location.objects.get_or_create(
        slug=d["slug"],
        defaults={
            "designation": d["designation"],
            "address":     d["address"],
            "locality":    locality_obj,
            "website":     d.get("website"),
            "phone":       d.get("phone"),
            "capacity":    d.get("capacity", 200),
        },
    )
    locations_objs[d["designation"]] = obj
    print(f"  {'[+]' if created else '[ ]'} {d['designation']}")

# Récupérer les lieux existants
for loc in Location.objects.all():
    locations_objs[loc.designation] = loc

print(f"  Total Locations : {Location.objects.count()}")


# ─────────────────────────────────────────────
# 5. ARTISTES
# ─────────────────────────────────────────────
print("\n[5/9] Artistes...")

artists_data = [
    ("Sophie",    "Deprez"),
    ("Marc",      "Delcourt"),
    ("Isabelle",  "Warnier"),
    ("Jean-Luc",  "Piraux"),
    ("Nathalie",  "Uffner"),
    ("Pierre",    "Bodson"),
    ("Catherine", "Claeys"),
    ("Antoine",   "Herbulot"),
]

artists_objs = {}
for firstname, lastname in artists_data:
    obj, created = Artist.objects.get_or_create(
        firstname=firstname, lastname=lastname
    )
    artists_objs[f"{firstname} {lastname}"] = obj
    print(f"  {'[+]' if created else '[ ]'} {firstname} {lastname}")

# Récupérer les artistes existants
for a in Artist.objects.all():
    artists_objs[f"{a.firstname} {a.lastname}"] = a

print(f"  Total Artists : {Artist.objects.count()}")


# ─────────────────────────────────────────────
# 6. ARTIST_TYPE (artiste ↔ type de spécialité)
# ─────────────────────────────────────────────
print("\n[6/9] Liaisons Artiste ↔ Type...")

# Récupérer les objets nécessaires
t_comedie  = types_objs.get("Comédie")
t_theatre  = types_objs.get("Théâtre")
t_drame    = types_objs.get("Drame")
t_one_man  = types_objs.get("One-man-show")
t_danse    = types_objs.get("Danse")
t_musique  = types_objs.get("Musique")
t_impro    = types_objs.get("Improvisation")

artist_type_map = [
    ("Sophie Deprez",      t_comedie),
    ("Sophie Deprez",      t_theatre),
    ("Marc Delcourt",      t_comedie),
    ("Marc Delcourt",      t_one_man),
    ("Isabelle Warnier",   t_theatre),
    ("Isabelle Warnier",   t_drame),
    ("Jean-Luc Piraux",    t_comedie),
    ("Jean-Luc Piraux",    t_impro),
    ("Nathalie Uffner",    t_theatre),
    ("Pierre Bodson",      t_comedie),
    ("Pierre Bodson",      t_theatre),
    ("Catherine Claeys",   t_danse),
    ("Catherine Claeys",   t_musique),
    ("Antoine Herbulot",   t_theatre),
    ("Antoine Herbulot",   t_drame),
    # Artistes existants — enrichissement
    ("Daniel Marcelin",    t_comedie),
    ("Philippe Laurent",   t_theatre),
]

at_objs = {}  # clé : (artist_id, type_id)
for artist_name, type_obj in artist_type_map:
    if type_obj is None:
        continue
    artist_obj = artists_objs.get(artist_name)
    if artist_obj is None:
        continue
    obj, created = ArtistType.objects.get_or_create(
        artist=artist_obj, type=type_obj
    )
    at_objs[(artist_obj.id, type_obj.id)] = obj
    print(f"  {'[+]' if created else '[ ]'} {artist_name} ↔ {type_obj.type}")

print(f"  Total ArtistType : {ArtistType.objects.count()}")


# ─────────────────────────────────────────────
# 7. ARTIST_TYPE_SHOW (artiste ↔ spectacle)
# ─────────────────────────────────────────────
print("\n[7/9] Liaisons Artiste ↔ Spectacle...")

# On récupère les spectacles existants par titre
shows_dict = {s.title: s for s in Show.objects.all()}

def link_artist_to_show(artist_name, type_name, show_title):
    """Crée la liaison ArtistTypeShow si elle n'existe pas encore."""
    artist = artists_objs.get(artist_name)
    t      = types_objs.get(type_name)
    show   = shows_dict.get(show_title)
    if not all([artist, t, show]):
        print(f"  [!] Impossible : {artist_name} | {type_name} | {show_title}")
        return

    at, _ = ArtistType.objects.get_or_create(artist=artist, type=t)
    obj, created = ArtistTypeShow.objects.get_or_create(artist_type=at, show=show)
    print(f"  {'[+]' if created else '[ ]'} {artist_name} ({type_name}) → {show_title}")

# Chaque spectacle reçoit 2-3 artistes réalistes
links = [
    # Le Prénom — comédie de Matthieu Delaporte
    ("Sophie Deprez",    "Comédie",   "Le Prénom"),
    ("Marc Delcourt",    "Comédie",   "Le Prénom"),
    ("Jean-Luc Piraux",  "Comédie",   "Le Prénom"),

    # Edmond — autour d'Edmond Rostand
    ("Isabelle Warnier", "Théâtre",   "Edmond"),
    ("Antoine Herbulot", "Théâtre",   "Edmond"),
    ("Pierre Bodson",    "Comédie",   "Edmond"),

    # Le Dîner de Cons — comédie de Francis Veber
    ("Marc Delcourt",    "Comédie",   "Le Dîner de Cons"),
    ("Jean-Luc Piraux",  "Comédie",   "Le Dîner de Cons"),
    ("Pierre Bodson",    "Comédie",   "Le Dîner de Cons"),

    # Boeing Boeing — farce de Marc Camoletti
    ("Sophie Deprez",    "Comédie",   "Boeing Boeing"),
    ("Marc Delcourt",    "Comédie",   "Boeing Boeing"),

    # Toc Toc — comédie de Laurent Baffie
    ("Jean-Luc Piraux",  "Improvisation", "Toc Toc"),
    ("Catherine Claeys", "Danse",         "Toc Toc"),
    ("Nathalie Uffner",  "Théâtre",       "Toc Toc"),

    # Silence on tourne
    ("Isabelle Warnier", "Théâtre",   "Silence on tourne"),
    ("Antoine Herbulot", "Drame",     "Silence on tourne"),

    # Intramuros
    ("Nathalie Uffner",  "Théâtre",   "Intramuros"),
    ("Pierre Bodson",    "Théâtre",   "Intramuros"),
]

for artist_name, type_name, show_title in links:
    link_artist_to_show(artist_name, type_name, show_title)

print(f"  Total ArtistTypeShow : {ArtistTypeShow.objects.count()}")


# ─────────────────────────────────────────────
# 8. USER META + PROFILES
# ─────────────────────────────────────────────
print("\n[8/9] UserMeta & Profiles...")

user_extra = [
    ("admin",      "fr"),
    ("hicham",     "fr"),
    ("hicham2026", "nl"),
]

for username, langue in user_extra:
    user = User.objects.filter(username=username).first()
    if not user:
        continue

    # UserMeta
    _, created_meta = UserMeta.objects.get_or_create(user=user, defaults={"langue": langue})
    print(f"  {'[+]' if created_meta else '[ ]'} UserMeta : {username} ({langue})")

    # Profile (photo de profil)
    _, created_prof = Profile.objects.get_or_create(user=user, defaults={"image": "default.jpg"})
    print(f"  {'[+]' if created_prof else '[ ]'} Profile  : {username}")

print(f"  Total UserMeta  : {UserMeta.objects.count()}")
print(f"  Total Profiles  : {Profile.objects.count()}")


# ─────────────────────────────────────────────
# 9. RÉSERVATIONS & AVIS
# ─────────────────────────────────────────────
print("\n[9/9] Réservations & Avis...")

hicham     = User.objects.filter(username="hicham").first()
hicham2026 = User.objects.filter(username="hicham2026").first()
admin_user = User.objects.filter(username="admin").first()

# Prendre quelques représentations existantes
reps = list(Representation.objects.select_related('show').all())

if len(reps) >= 5 and hicham:
    reservations_to_add = [
        (hicham,     reps[0],  2),
        (hicham,     reps[5],  1),
        (hicham,     reps[10], 3),
        (hicham2026, reps[2],  4),
        (hicham2026, reps[7],  2),
        (admin_user, reps[15], 1),
    ]
    for user, rep, places in reservations_to_add:
        if user is None:
            continue
        # On évite les doublons (même user + même représentation)
        exists = Reservation.objects.filter(user=user, representation=rep).exists()
        if not exists:
            Reservation.objects.create(user=user, representation=rep, places=places)
            print(f"  [+] Réservation : {user.username} → {rep.show.title} ({places} place(s))")
        else:
            print(f"  [ ] Déjà existante : {user.username} → {rep.show.title}")

# Avis réalistes
reviews_to_add = [
    (hicham,     "Le Prénom",      4, "Excellent spectacle, le texte est très bien écrit. Les acteurs sont convaincants.", True),
    (hicham,     "Le Dîner de Cons", 5, "Un classique incontournable ! On rit du début à la fin, le timing comique est parfait.", True),
    (hicham2026, "Edmond",         4, "Belle mise en scène, très fidèle à l'esprit de Rostand. Quelques longueurs dans le deuxième acte.", True),
    (hicham2026, "Toc Toc",        5, "J'ai adoré ! Les six personnages sont tous attachants et les situations sont hilarantes.", True),
    (admin_user, "Boeing Boeing",  3, "Bonne comédie de boulevard, sans grande surprise mais agréable à regarder.", True),
    (admin_user, "Intramuros",     4, "Un spectacle touchant et bien interprété. La salle était comble, c'est mérité.", True),
    (hicham,     "Silence on tourne", 5, "Superbe ! La direction d'acteurs est impeccable, on est transporté.", False),
]

for user, show_title, stars, text, validated in reviews_to_add:
    if user is None:
        continue
    show = shows_dict.get(show_title)
    if show is None:
        # Cherche le titre avec encodage différent
        for k, v in shows_dict.items():
            if show_title.lower() in k.lower():
                show = v
                break
    if show is None:
        print(f"  [!] Show introuvable : {show_title}")
        continue

    exists = Review.objects.filter(user=user, show=show).exists()
    if not exists:
        Review.objects.create(
            user=user, show=show,
            stars=stars, review=text, validated=validated,
        )
        status = "validé" if validated else "en attente"
        print(f"  [+] Avis ({status}) : {user.username} → {show.title} ({stars}★)")
    else:
        print(f"  [ ] Avis déjà existant : {user.username} → {show.title}")

print(f"  Total Reservations : {Reservation.objects.count()}")
print(f"  Total Reviews      : {Review.objects.count()}")


# ─────────────────────────────────────────────
# RÉSUMÉ FINAL
# ─────────────────────────────────────────────
print("\n" + "="*55)
print("  RÉSUMÉ FINAL")
print("="*55)
models_summary = [
    ("Users",          User.objects.count()),
    ("Groups",         Group.objects.count()),
    ("Types",          Type.objects.count()),
    ("Roles",          Role.objects.count()),
    ("Localities",     Locality.objects.count()),
    ("Locations",      Location.objects.count()),
    ("Artists",        Artist.objects.count()),
    ("ArtistType",     ArtistType.objects.count()),
    ("Shows",          Show.objects.count()),
    ("ArtistTypeShow", ArtistTypeShow.objects.count()),
    ("Representations",Representation.objects.count()),
    ("Reservations",   Reservation.objects.count()),
    ("Profiles",       Profile.objects.count()),
    ("UserMeta",       UserMeta.objects.count()),
    ("Reviews",        Review.objects.count()),
]
for name, count in models_summary:
    bar = "✅" if count >= 3 else ("🟡" if count >= 1 else "🔴")
    print(f"  {bar}  {name:<20} {count:>3} entrée(s)")

print("="*55)
print("  Seed terminé avec succès !")
print("="*55 + "\n")
