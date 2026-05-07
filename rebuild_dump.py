# -*- coding: utf-8 -*-
"""
rebuild_dump.py — Regénère un dump propre avec tous les accents corrects.

Stratégie : on réinitialise TOUTES les valeurs accentuées directement
via UNHEX (bytecode SQL) pour court-circuiter tout problème de connexion,
puis on génère le dump mysqldump.

Usage : python rebuild_dump.py  (depuis le répertoire du projet)
"""
import os
import subprocess
import sys

# ── 1. Correction des données en base via raw SQL UNHEX ────────────────────
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from django.db import connection

# Valeurs correctes encodées en UTF-8 hex (pour éviter tout problème de connexion)
# Générées avec : s.encode('utf-8').hex().upper()

def utf8hex(s):
    return s.encode('utf-8').hex().upper()

# Toutes les corrections à appliquer (table, id, colonne, valeur correcte)
corrections = {
    'types': [
        (2, 'type', 'Comédie'),
        (3, 'type', 'Théâtre'),
    ],
    'roles': [
        (4, 'role', 'Metteur en scène'),
        (5, 'role', 'Metteuse en scène'),
        (6, 'role', 'Comédien'),
        (7, 'role', 'Comédienne'),
    ],
    'locations': [
        (3, 'designation', "Théâtre de la Toison d'Or"),
        (3, 'address',     "Galeries de la Toison d'Or 396"),
        (4, 'designation', 'Théâtre National de Bruxelles'),
        (5, 'designation', 'Théâtre Les Riches Claires'),
        (6, 'designation', 'Théâtre Royal du Parc'),
    ],
}

print("=== RESET via UNHEX (bypass connexion) ===")
with connection.cursor() as c:
    c.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table, rows in corrections.items():
        for row_id, col, val in rows:
            hex_val = utf8hex(val)
            sql = f"UPDATE `{table}` SET `{col}` = CONVERT(UNHEX('{hex_val}') USING utf8mb4) WHERE id = {row_id}"
            c.execute(sql)
            print(f"  [OK] {table}[{row_id}].{col} => {val}")
    c.execute("SET FOREIGN_KEY_CHECKS = 1")

# ── 2. Vérification HEX ────────────────────────────────────────────────────
print("\n=== Vérification HEX ===")
checks = [
    ("SELECT id, HEX(`type`) FROM types WHERE id IN (2,3)", "types"),
    ("SELECT id, HEX(`role`) FROM roles WHERE id IN (4,5,6,7)", "roles"),
    ("SELECT id, HEX(`designation`) FROM locations WHERE id IN (3,4,5,6)", "locations"),
]
with connection.cursor() as c:
    for sql, label in checks:
        c.execute(sql)
        for row in c.fetchall():
            raw = bytes.fromhex(row[1])
            try:
                decoded = raw.decode('utf-8')
            except Exception:
                decoded = raw.decode('latin-1') + ' [LATIN-1!]'
            status = "✓" if '�' not in decoded and 'Ã' not in decoded else "✗"
            print(f"  {status} {label}[{row[0]}]: {decoded!r}")

print("\nBase corrigée. Lance maintenant le mysqldump manuellement.")
print("Commande suggérée (depuis PowerShell) :")
print(r"""
  $tables = "artists types localities roles locations shows representations reservations artist_type artist_type_show profiles user_meta reviews auth_user auth_group auth_user_groups"
  $dump = & "C:\xampp\mysql\bin\mysqldump.exe" --user=rooot --password=rooot --host=127.0.0.1 --port=3306 --default-character-set=utf8mb4 --no-tablespaces --single-transaction --add-drop-table --complete-insert reservations $tables.Split(" ")
  [System.IO.File]::WriteAllText("C:\Users\HP\reservations\dump_reservations.sql", ($dump -join "`n"), [System.Text.Encoding]::UTF8)
""")
