# -*- coding: utf-8 -*-
"""Vérifie les octets réels des titres pour détecter tout problème d'encodage."""
from django.db import connection

with connection.cursor() as c:
    c.execute("SELECT slug, title, HEX(title) FROM `shows` WHERE slug IN ('le-prenom','le-diner-de-cons')")
    for slug, title, hexa in c.fetchall():
        print(f"slug  : {slug}")
        print(f"title : {title!r}")
        print(f"HEX   : {hexa}")
        # Décode les hex bytes pour voir le contenu réel
        try:
            raw = bytes.fromhex(hexa).decode('utf-8')
            print(f"UTF-8 : {raw}")
        except Exception as e:
            try:
                raw = bytes.fromhex(hexa).decode('latin-1')
                print(f"latin1: {raw}")
            except Exception as e2:
                print(f"Erreur décodage: {e2}")
        print()
