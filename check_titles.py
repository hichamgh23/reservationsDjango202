# -*- coding: utf-8 -*-
from django.db import connection
with connection.cursor() as c:
    c.execute('SELECT slug, title FROM `shows` ORDER BY id')
    print('Titres actuels en base :')
    for row in c.fetchall():
        print(f'  {row[0]!s:<35} | {row[1]!s}')
