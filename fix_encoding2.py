# -*- coding: utf-8 -*-
"""
fix_encoding2.py — Correction des données originales en latin1 converties incorrectement

Les données chargées depuis les fixtures (loaddata) étaient en latin1 (bytes simples :
E9 pour é, E2 pour â, E8 pour è). Lors de CONVERT TO CHARACTER SET utf8mb4, MariaDB
a réinterprété ces bytes comme latin1 et les a re-encodés en UTF-8. On les corrige.
"""
from django.db import connection

# Toutes les valeurs à corriger, repérées par leur id
location_fixes = [
    (3, 'designation', "Théâtre de la Toison d'Or"),
    (3, 'address',     "Galeries de la Toison d'Or 396"),
]

# Vérifier les autres tables : localities, shows, descriptions, etc.
locality_fixes = []  # Bruxelles, Watermael-Boitsfort : pas d'accents problématiques

# Vérification HEX avant correction
with connection.cursor() as c:
    c.execute("SELECT id, HEX(designation), designation FROM locations WHERE id = 3")
    row = c.fetchone()
    print(f"AVANT — locations[3]: HEX={row[1]}")
    try:
        decoded = bytes.fromhex(row[1]).decode('latin-1')
        print(f"  lu en latin-1 : {decoded!r}")
    except Exception as e:
        print(f"  erreur: {e}")

print("\n=== Corrections locations originales ===")
with connection.cursor() as c:
    for row_id, col, val in location_fixes:
        c.execute(f"UPDATE `locations` SET `{col}` = %s WHERE id = %s", [val, row_id])
        print(f"  [OK] locations[{row_id}].{col} => {val}")

# Vérification finale HEX
with connection.cursor() as c:
    c.execute("SELECT id, HEX(designation), designation FROM locations WHERE id = 3")
    row = c.fetchone()
    print(f"\nAPRES — locations[3]: HEX={row[1]}")
    print(f"  valeur : {row[2]!r}")

# Vérifier aussi les reviews et descriptions de shows
print("\n=== Vérification reviews (textes) ===")
with connection.cursor() as c:
    c.execute("SELECT id, user_id, show_id, stars, LEFT(review, 60) FROM reviews ORDER BY id")
    for row in c.fetchall():
        print(f"  [{row[0]}] user={row[1]} show={row[2]} stars={row[3]} | {row[4]!r}")

print("\nDone.")
