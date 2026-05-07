# -*- coding: utf-8 -*-
"""
fix_encoding.py — Correction des données doublement encodées (mojibake)

Problème : seed_data.py a été exécuté avant que charset=utf8mb4 soit configuré
dans settings.py. Les accents (é, è, â) ont été stockés en double UTF-8.
Ce script les remet à la bonne valeur via UPDATE ciblé par ID.
"""
from django.db import connection

fixes = [
    # (table, id, colonne, valeur_correcte)
    # --- Types ---
    ('types',     2, 'type',        'Comédie'),
    ('types',     3, 'type',        'Théâtre'),

    # --- Roles ---
    ('roles',     4, 'role',        'Metteur en scène'),
    ('roles',     5, 'role',        'Metteuse en scène'),
    ('roles',     6, 'role',        'Comédien'),
    ('roles',     7, 'role',        'Comédienne'),

    # --- Locations (nouvelles salles ajoutées par seed_data.py) ---
    ('locations', 4, 'designation', 'Théâtre National de Bruxelles'),
    ('locations', 5, 'designation', 'Théâtre Les Riches Claires'),
    ('locations', 6, 'designation', 'Théâtre Royal du Parc'),
]

print("\n=== Correction des encodages ===")
with connection.cursor() as c:
    for table, row_id, col, correct_value in fixes:
        c.execute(
            f"UPDATE `{table}` SET `{col}` = %s WHERE id = %s",
            [correct_value, row_id]
        )
        print(f"  [OK] {table}[{row_id}].{col} => {correct_value}")

print("\n=== Verification ===")
with connection.cursor() as c:
    for table, col in [('types','type'), ('roles','role'), ('locations','designation')]:
        c.execute(f"SELECT id, `{col}` FROM `{table}` ORDER BY id")
        print(f"\n  {table}.{col}:")
        for row in c.fetchall():
            print(f"    [{row[0]}] {row[1]!r}")

print("\nDone.")
