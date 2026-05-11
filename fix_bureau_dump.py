# -*- coding: utf-8 -*-
INPUT  = r"C:\Users\HP\Desktop\dump_reservations.sql"
OUTPUT = r"C:\Users\HP\Desktop\dump_reservations.sql"

DOUBLE = [
    ('ÃÂ©', 'é'), ('ÃÂ¨', 'è'), ('ÃÂª', 'ê'), ('ÃÂ«', 'ë'),
    ('ÃÂ¢', 'â'), ('ÃÂ®', 'î'), ('ÃÂ¯', 'ï'), ('ÃÂ´', 'ô'),
    ('ÃÂ»', 'û'), ('ÃÂ§', 'ç'), ('ÃÂ¹', 'ù'), ('ÃÂ¼', 'ü'),
    ('ÃÂ\xa0', 'à'), ('ÃÂ ', 'à'),
    ('ÃÂ‰', 'É'), ('ÃÂˆ', 'È'), ('ÃÂ€', 'À'),
]
SIMPLE = [
    ('Ã©', 'é'), ('Ã¨', 'è'), ('Ãª', 'ê'), ('Ã¢', 'â'),
    ('Ã®', 'î'), ('Ã´', 'ô'), ('Ã»', 'û'), ('Ã§', 'ç'),
    ('Ã\xa0', 'à'), ('Ã ', 'à'), ('Ã¹', 'ù'), ('Ã¼', 'ü'),
    ('Ã‰', 'É'), ('Ãˆ', 'È'), ('Ã€', 'À'),
]

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

total = 0
for wrong, right in DOUBLE + SIMPLE:
    n = content.count(wrong)
    if n:
        content = content.replace(wrong, right)
        total += n

with open(OUTPUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

import re
remaining = re.findall(r'Ã.', content)
print(f"Corrections : {total}")
print("Resultat : " + ("PROPRE" if not remaining else f"residuels: {set(remaining)}"))
