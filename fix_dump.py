# -*- coding: utf-8 -*-
"""
fix_dump.py — Corrige le mojibake dans le fichier dump SQL

Problème : mysqldump lit les données via une connexion latin1 même avec
--default-character-set=utf8mb4 sur MariaDB 10.x (bug connu).
Les bytes UTF-8 des accents (C3 A9 pour é) sont lus comme deux chars latin1
(Ã et ©) puis réencodés en UTF-8 dans le dump (C3 83 C2 A9).

Fix : on remplace chaque séquence Ã+char par l'accentuée correcte.
"""

REPLACEMENTS = {
    # Minuscules accentuées communes (français)
    'Ã©': 'é',   # é
    'Ã¨': 'è',   # è
    'Ãª': 'ê',   # ê
    'Ã«': 'ë',   # ë
    'Ã ': 'à',   # à (Ã suivi d'espace insécable latin1 0xA0)
    'Ã¢': 'â',   # â
    'Ã¤': 'ä',   # ä
    'Ã®': 'î',   # î
    'Ã¯': 'ï',   # ï
    'Ã´': 'ô',   # ô
    'Ã¶': 'ö',   # ö
    'Ã¹': 'ù',   # ù
    'Ã»': 'û',   # û
    'Ã¼': 'ü',   # ü
    'Ã§': 'ç',   # ç
    # Majuscules accentuées
    'Ã‰': 'É',   # É
    'Ãˆ': 'È',   # È
    'Ã€': 'À',   # À
    'Ã‚': 'Â',   # Â
    'Ã®': 'Î',   # Î
    'Å': 'Œ',   # Œ
    'Å': 'œ',   # œ
}

dump_path = r'C:\Users\HP\reservations\dump_reservations.sql'

with open(dump_path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content
count_total = 0
for wrong, right in REPLACEMENTS.items():
    n = content.count(wrong)
    if n:
        content = content.replace(wrong, right)
        count_total += n
        print(f"  {n:3d}x {wrong!r} = {right!r}")

with open(dump_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f"\n  {count_total} remplacements effectués dans le dump.")
print(f"  Fichier réécrit : {dump_path}")

# Vérification : cherche les Ã résiduels
residual = [line for line in content.split('\n') if 'Ã' in line]
if residual:
    print(f"\n  ⚠ {len(residual)} ligne(s) avec Ã résiduel :")
    for l in residual[:5]:
        print(f"    {l[:120]}")
else:
    print("\n  ✓ Aucun Ã résiduel — dump propre.")
