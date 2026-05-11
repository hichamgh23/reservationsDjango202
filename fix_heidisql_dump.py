# -*- coding: utf-8 -*-
"""
fix_heidisql_dump.py — Corrige les accents corrompus dans le dump HeidiSQL

HeidiSQL exporte parfois les accents en double/triple encodage.
Ce script corrige les patterns connus et produit un dump propre.
"""

import re

# Fichier à corriger — modifie ce chemin si le dump est ailleurs
INPUT  = r"C:\Users\HP\reservations\dump_reservations.sql"
OUTPUT = r"C:\Users\HP\reservations\dump_reservations_clean.sql"

# ── Pattern double : ÃÂ + char (utilisé dans les données HeidiSQL) ──────────
DOUBLE = [
    ('ÃÂ©', 'é'),  # é
    ('ÃÂ¨', 'è'),  # è
    ('ÃÂª', 'ê'),  # ê
    ('ÃÂ«', 'ë'),  # ë
    ('ÃÂ¢', 'â'),  # â
    ('ÃÂ®', 'î'),  # î
    ('ÃÂ¯', 'ï'),  # ï
    ('ÃÂ´', 'ô'),  # ô
    ('ÃÂ»', 'û'),  # û
    ('ÃÂ§', 'ç'),  # ç
    ('ÃÂ\xa0', 'à'),  # à (suivi d'espace insécable)
    ('ÃÂ ', 'à'),   # à (suivi d'espace normal)
    ('ÃÂ¹', 'ù'),  # ù
    ('ÃÂ¼', 'ü'),  # ü
    ('ÃÂ‰', 'É'),  # É
    ('ÃÂˆ', 'È'),  # È
    ('ÃÂ€', 'À'),  # À
]

# ── Pattern simple : Ã + char (utilisé dans les commentaires HeidiSQL) ───────
SIMPLE = [
    ('Ã©', 'é'),
    ('Ã¨', 'è'),
    ('Ãª', 'ê'),
    ('Ã¢', 'â'),
    ('Ã®', 'î'),
    ('Ã´', 'ô'),
    ('Ã»', 'û'),
    ('Ã§', 'ç'),
    ('Ã\xa0', 'à'),
    ('Ã ', 'à'),
    ('Ã¹', 'ù'),
    ('Ã¼', 'ü'),
    ('Ã‰', 'É'),
    ('Ãˆ', 'È'),
    ('Ã€', 'À'),
]

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

total = 0

# On applique d'abord le pattern double (le plus long, prioritaire)
for wrong, right in DOUBLE:
    n = content.count(wrong)
    if n:
        content = content.replace(wrong, right)
        total += n

# Puis le pattern simple
for wrong, right in SIMPLE:
    n = content.count(wrong)
    if n:
        content = content.replace(wrong, right)
        total += n

with open(OUTPUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# Vérification
remaining = re.findall(r'Ã.', content)
print(f"{total} correction(s) effectuée(s)")
if remaining:
    print(f"Sequences Ã résiduelles ({len(remaining)}) :", set(remaining))
else:
    print("Dump propre — aucun accent résiduel.")
print(f"Fichier corrigé : {OUTPUT}")
