from django.db import migrations
from django.utils.text import slugify
from datetime import datetime, timedelta

def seed_complete_data(apps, schema_editor):
    # Récupération des modèles via l'historique des migrations
    Show = apps.get_model('catalogue', 'Show')
    Location = apps.get_model('catalogue', 'Location')
    Locality = apps.get_model('catalogue', 'Locality')
    
    # On tente de récupérer le modèle pour les dates
    # Si ton modèle s'appelle autrement (ex: 'ShowDate'), change-le ici
    try:
        Representation = apps.get_model('catalogue', 'Representation')
    except LookupError:
        Representation = None

    # 1. CRÉATION DU LIEU (Obligatoire pour lier les spectacles)
    bru, _ = Locality.objects.get_or_create(
        postal_code="1000", 
        defaults={'locality': "Bruxelles"}
    )
    
    tto, _ = Location.objects.get_or_create(
        slug="tto",
        defaults={
            'designation': "Théâtre de la Toison d'Or",
            'address': "Galeries de la Toison d'Or 396, 1050 Ixelles",
            'locality': bru
        }
    )

    # 2. LISTE DES 10 SPECTACLES (Style TTO / Utick)
    spectacles_list = [
        ("C'est fini pour moi", 25.00, "https://images.unsplash.com/photo-1503095396549-807039045047?w=800"),
        ("Le Prénom", 30.00, "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=800"),
        ("Silence on tourne", 22.50, "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800"),
        ("Edmond", 28.00, "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800"),
        ("Ladies Night", 26.00, "https://images.unsplash.com/photo-1514525253361-bee243870d22?w=800"),
        ("Le Dîner de Cons", 24.00, "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800"),
        ("Boeing Boeing", 20.00, "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800"),
        ("Toc Toc", 23.00, "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800"),
        ("Le Porteur d'Histoire", 27.50, "https://images.unsplash.com/photo-1460662192681-ebca326f6337?w=800"),
        ("Intramuros", 29.00, "https://images.unsplash.com/photo-1507915135761-41a0a222c709?w=800"),
    ]

    # 3. CRÉATION DES SPECTACLES + 4 DATES CHACUN
    # Date de départ : 1er Avril 2026
    start_date = datetime(2026, 4, 1, 20, 0)

    for index, (title, price, img) in enumerate(spectacles_list):
        # Création ou récupération du spectacle
        show, created = Show.objects.get_or_create(
            slug=slugify(title),
            defaults={
                'title': title,
                'description': f"Venez découvrir {title}, une pièce unique dans le pur style du Théâtre de la Toison d'Or.",
                'poster_url': img,
                'price': price,
                'bookable': True,
                'location': tto
            }
        )

        # Si le modèle Representation existe, on ajoute 4 dates
        if Representation:
            for i in range(4):
                # On espace les dates : chaque spectacle a ses propres dates
                rep_when = start_date + timedelta(days=(index * 2) + (i * 7))
                Representation.objects.get_or_create(
                    show=show,
                    when=rep_when,
                    defaults={'location': tto}
                )

class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_profile'), # Ta dernière migration connue
    ]

    operations = [
        migrations.RunPython(seed_complete_data),
    ]
