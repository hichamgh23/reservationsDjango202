"""
fix_schema.py — Correction du schéma MySQL pour conformité évaluation

Corrections appliquées :
  1. Ajout ON DELETE + ON UPDATE sur toutes les clés étrangères
  2. Conversion charset utf8mb3 → utf8mb4 (correcte gestion des accents/emoji)
  3. Ajout CHECK stars BETWEEN 1 AND 5 sur reviews
  4. Ajout CHECK places >= 1 sur reservations
  5. Ajout UNIQUE KEY (artist_id, type_id) sur artist_type
  6. Ajout UNIQUE KEY (artist_type_id, show_id) sur artist_type_show

Usage : python manage.py shell -c "exec(open('fix_schema.py').read())"
"""

from django.db import connection

def run(sql, label=""):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print(f"  [OK] {label}")
    except Exception as e:
        print(f"  [!!] {label} → {e}")


print("\n" + "="*60)
print("  CORRECTION DU SCHEMA MySQL")
print("="*60)

# ─────────────────────────────────────────────────────────────
# 0. DESACTIVATION TEMPORAIRE DES FK CHECKS (pour les ALTER)
# ─────────────────────────────────────────────────────────────
run("SET FOREIGN_KEY_CHECKS = 0", "Désactivation FK checks")


# ─────────────────────────────────────────────────────────────
# 1. TABLE LOCATIONS
#    locality_id → ON DELETE SET NULL ON UPDATE CASCADE
# ─────────────────────────────────────────────────────────────
print("\n[locations]")
run("ALTER TABLE `locations` DROP FOREIGN KEY `locations_locality_id_22dd0b44_fk_localities_id`",
    "DROP FK locality_id")
run("""
    ALTER TABLE `locations`
    ADD CONSTRAINT `fk_locations_locality`
    FOREIGN KEY (`locality_id`) REFERENCES `localities`(`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
""", "ADD FK locality_id → SET NULL / CASCADE")


# ─────────────────────────────────────────────────────────────
# 2. TABLE SHOWS
#    location_id → ON DELETE SET NULL ON UPDATE CASCADE
# ─────────────────────────────────────────────────────────────
print("\n[shows]")
run("ALTER TABLE `shows` DROP FOREIGN KEY `shows_location_id_a6832141_fk_locations_id`",
    "DROP FK location_id")
run("""
    ALTER TABLE `shows`
    ADD CONSTRAINT `fk_shows_location`
    FOREIGN KEY (`location_id`) REFERENCES `locations`(`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
""", "ADD FK location_id → SET NULL / CASCADE")


# ─────────────────────────────────────────────────────────────
# 3. TABLE REPRESENTATIONS
#    show_id     → ON DELETE CASCADE ON UPDATE CASCADE
#    location_id → ON DELETE SET NULL ON UPDATE CASCADE
# ─────────────────────────────────────────────────────────────
print("\n[representations]")
run("ALTER TABLE `representations` DROP FOREIGN KEY `representations_show_id_90b07717_fk_shows_id`",
    "DROP FK show_id")
run("ALTER TABLE `representations` DROP FOREIGN KEY `representations_location_id_860c4ba1_fk_locations_id`",
    "DROP FK location_id")
run("""
    ALTER TABLE `representations`
    ADD CONSTRAINT `fk_representations_show`
    FOREIGN KEY (`show_id`) REFERENCES `shows`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK show_id → CASCADE / CASCADE")
run("""
    ALTER TABLE `representations`
    ADD CONSTRAINT `fk_representations_location`
    FOREIGN KEY (`location_id`) REFERENCES `locations`(`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
""", "ADD FK location_id → SET NULL / CASCADE")


# ─────────────────────────────────────────────────────────────
# 4. TABLE RESERVATIONS
#    representation_id → ON DELETE CASCADE ON UPDATE CASCADE
#    user_id           → ON DELETE CASCADE ON UPDATE CASCADE
#    CHECK places >= 1
# ─────────────────────────────────────────────────────────────
print("\n[reservations]")
run("ALTER TABLE `reservations` DROP FOREIGN KEY `reservations_representation_id_5f66501d_fk_representations_id`",
    "DROP FK representation_id")
run("ALTER TABLE `reservations` DROP FOREIGN KEY `reservations_user_id_d03abc5b_fk_auth_user_id`",
    "DROP FK user_id")
run("""
    ALTER TABLE `reservations`
    ADD CONSTRAINT `fk_reservations_representation`
    FOREIGN KEY (`representation_id`) REFERENCES `representations`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK representation_id → CASCADE / CASCADE")
run("""
    ALTER TABLE `reservations`
    ADD CONSTRAINT `fk_reservations_user`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK user_id → CASCADE / CASCADE")
# Supprimer l'ancien CHECK et en ajouter un plus strict
run("ALTER TABLE `reservations` DROP CHECK `reservations_chk_1`", "DROP CHECK places >= 0")
run("ALTER TABLE `reservations` ADD CONSTRAINT `chk_reservations_places` CHECK (`places` >= 1)",
    "ADD CHECK places >= 1")


# ─────────────────────────────────────────────────────────────
# 5. TABLE ARTIST_TYPE
#    artist_id → ON DELETE CASCADE ON UPDATE CASCADE
#    type_id   → ON DELETE CASCADE ON UPDATE CASCADE
#    UNIQUE (artist_id, type_id)
# ─────────────────────────────────────────────────────────────
print("\n[artist_type]")
run("ALTER TABLE `artist_type` DROP FOREIGN KEY `artist_type_artist_id_149b3981_fk_artists_id`",
    "DROP FK artist_id")
run("ALTER TABLE `artist_type` DROP FOREIGN KEY `artist_type_type_id_ddfedbec_fk_types_id`",
    "DROP FK type_id")
run("""
    ALTER TABLE `artist_type`
    ADD CONSTRAINT `fk_artist_type_artist`
    FOREIGN KEY (`artist_id`) REFERENCES `artists`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK artist_id → CASCADE / CASCADE")
run("""
    ALTER TABLE `artist_type`
    ADD CONSTRAINT `fk_artist_type_type`
    FOREIGN KEY (`type_id`) REFERENCES `types`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK type_id → CASCADE / CASCADE")
run("ALTER TABLE `artist_type` ADD UNIQUE KEY `uq_artist_type` (`artist_id`, `type_id`)",
    "ADD UNIQUE (artist_id, type_id)")


# ─────────────────────────────────────────────────────────────
# 6. TABLE ARTIST_TYPE_SHOW
#    artist_type_id → ON DELETE CASCADE ON UPDATE CASCADE
#    show_id        → ON DELETE CASCADE ON UPDATE CASCADE
#    UNIQUE (artist_type_id, show_id)
# ─────────────────────────────────────────────────────────────
print("\n[artist_type_show]")
run("ALTER TABLE `artist_type_show` DROP FOREIGN KEY `artist_type_show_artist_type_id_a12f3364_fk_artist_type_id`",
    "DROP FK artist_type_id")
run("ALTER TABLE `artist_type_show` DROP FOREIGN KEY `artist_type_show_show_id_656adc7c_fk_shows_id`",
    "DROP FK show_id")
run("""
    ALTER TABLE `artist_type_show`
    ADD CONSTRAINT `fk_ats_artist_type`
    FOREIGN KEY (`artist_type_id`) REFERENCES `artist_type`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK artist_type_id → CASCADE / CASCADE")
run("""
    ALTER TABLE `artist_type_show`
    ADD CONSTRAINT `fk_ats_show`
    FOREIGN KEY (`show_id`) REFERENCES `shows`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK show_id → CASCADE / CASCADE")
run("ALTER TABLE `artist_type_show` ADD UNIQUE KEY `uq_artist_type_show` (`artist_type_id`, `show_id`)",
    "ADD UNIQUE (artist_type_id, show_id)")


# ─────────────────────────────────────────────────────────────
# 7. TABLE PROFILES
#    user_id → ON DELETE CASCADE ON UPDATE CASCADE (OneToOne)
# ─────────────────────────────────────────────────────────────
print("\n[profiles]")
run("ALTER TABLE `profiles` DROP FOREIGN KEY `profiles_user_id_36580373_fk_auth_user_id`",
    "DROP FK user_id")
run("""
    ALTER TABLE `profiles`
    ADD CONSTRAINT `fk_profiles_user`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK user_id → CASCADE / CASCADE")


# ─────────────────────────────────────────────────────────────
# 8. TABLE USER_META
#    user_id → ON DELETE CASCADE ON UPDATE CASCADE (OneToOne)
# ─────────────────────────────────────────────────────────────
print("\n[user_meta]")
run("ALTER TABLE `user_meta` DROP FOREIGN KEY `user_meta_user_id_58c29229_fk_auth_user_id`",
    "DROP FK user_id")
run("""
    ALTER TABLE `user_meta`
    ADD CONSTRAINT `fk_user_meta_user`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
""", "ADD FK user_id → CASCADE / CASCADE")


# ─────────────────────────────────────────────────────────────
# 9. TABLE REVIEWS
#    show_id → ON DELETE RESTRICT ON UPDATE CASCADE
#    user_id → ON DELETE RESTRICT ON UPDATE CASCADE
#    CHECK stars BETWEEN 1 AND 5
# ─────────────────────────────────────────────────────────────
print("\n[reviews]")
run("ALTER TABLE `reviews` DROP FOREIGN KEY `reviews_show_id_53c4ca85_fk_shows_id`",
    "DROP FK show_id")
run("ALTER TABLE `reviews` DROP FOREIGN KEY `reviews_user_id_c23b0903_fk_auth_user_id`",
    "DROP FK user_id")
run("""
    ALTER TABLE `reviews`
    ADD CONSTRAINT `fk_reviews_show`
    FOREIGN KEY (`show_id`) REFERENCES `shows`(`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
""", "ADD FK show_id → RESTRICT / CASCADE")
run("""
    ALTER TABLE `reviews`
    ADD CONSTRAINT `fk_reviews_user`
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
""", "ADD FK user_id → RESTRICT / CASCADE")
run("ALTER TABLE `reviews` DROP CHECK `reviews_chk_1`", "DROP CHECK stars >= 0")
run("""
    ALTER TABLE `reviews`
    ADD CONSTRAINT `chk_reviews_stars`
    CHECK (`stars` BETWEEN 1 AND 5)
""", "ADD CHECK stars BETWEEN 1 AND 5")


# ─────────────────────────────────────────────────────────────
# 10. CONVERSION CHARSET utf8mb3 → utf8mb4 (corrige les accents)
# ─────────────────────────────────────────────────────────────
print("\n[charset utf8mb3 → utf8mb4]")
tables_to_convert = [
    'artists', 'types', 'localities', 'roles', 'locations',
    'shows', 'representations', 'reservations',
    'artist_type', 'artist_type_show',
    'profiles', 'user_meta', 'reviews',
]
for tbl in tables_to_convert:
    run(f"ALTER TABLE `{tbl}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
        f"UTF8MB4 : {tbl}")


# ─────────────────────────────────────────────────────────────
# RÉACTIVATION DES FK CHECKS
# ─────────────────────────────────────────────────────────────
run("SET FOREIGN_KEY_CHECKS = 1", "Réactivation FK checks")

print("\n" + "="*60)
print("  SCHÉMA CORRIGÉ AVEC SUCCÈS")
print("="*60 + "\n")
