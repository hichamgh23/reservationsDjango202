from django.db import migrations
from django.utils.text import slugify
from datetime import datetime, timedelta

def seed_complete_data(apps, schema_editor):
    Show = apps.get_model('catalogue', 'Show')
    Location = apps.get_model('catalogue', 'Location')
    Locality = apps.get_model('catalogue', 'Locality')
    # Si tu as un modèle pour les dates, remplace 'Representation' par son nom exact
    # Sinon, le script créera au moins les spectacles.
    try:
        Representation = apps.get_model('catalogue', 'Representation')
    except LookupError:
        Representation = None

    # 1. Setup du lieu
    bru, _ = Locality.objects.get_or_create(postal_code="1000", locality="Bruxelles")
    tto, _ = Location.objects.get_or_create(
        slug="tto",
        designation="Théâtre de la Toison d'Or",
        address="Galeries de la Toison d'Or 396",
        locality=bru
    )

    # 2. Liste des 10 spectacles
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

    # 3. Création et ajout des dates
    base_date = datetime(2026, 3, 1, 20, 0) # 1er mars 2026 à 20h

    for title, price, img_url in spectacles_list:
        show, _ = Show.objects.get_or_create(
            slug=slugify(title),
            defaults={
                'title': title,
                'description': f"Une performance incroyable de {title} à ne pas manquer.",
                'poster_url': img_url,
                'price': price,
                'bookable': True,
                'location': tto
            }
        )

        # 4. Ajout de 4 dates par spectacle (si le modèle Representation existe)
        if Representation:
            for i in range(4):
                # On crée 4 dates espacées d'une semaine
                rep_date = base_date + timedelta(weeks=i, days=spectacles_list.index((title, price, img_url)))
                Representation.objects.get_or_create(
                    show=show,
                    when=rep_date,
                    location=tto
                )

class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_initial'), # REMPLACE PAR LE NOM DE TA MIGRATION PRECEDENTE
    ]

    operations = [
        migrations.RunPython(seed_complete_data),
    ]