from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    # Page d'accueil (doublon pour sécurité)
    path('', views.welcome, name='welcome'),

    # Catalogue des spectacles
    path('shows/', views.show_index, name='show_index'),

    # Détail d'un spectacle
    path('show/<int:show_id>/', views.show_detail, name='show_detail'),

    # Inscription
    path('signup/', views.signup, name='signup'),

    # Processus de réservation
    path('book/<int:representation_id>/', views.book_representation, name='book_representation'),
    path('profile/', views.profile, name='profile'),

    # Route pour l'annulation (suppression) d'une réservation
    path('reservation/<int:reservation_id>/delete/', views.reservation_delete, name='reservation_delete'),

    # --- AJOUTS POUR LA GESTION DU PROFIL ---
    
    # Changement de mot de passe
    path('profile/password/', views.change_password, name='change_password'),
    
    # Mise à jour de la photo de profil
    path('profile/update/', views.profile_update, name='profile_update'),
    
    # Suppression de la photo de profil
    path('profile/image/delete/', views.delete_profile_image, name='delete_profile_image'),

    # --- CRUD ARTIST ---
path('artist/', views.artist_index, name='artist_index'),
path('artist/create/', views.artist_create, name='artist_create'),
path('artist/<int:id>/', views.artist_show, name='artist_show'),
path('artist/<int:id>/edit/', views.artist_edit, name='artist_edit'),
path('artist/<int:id>/delete/', views.artist_delete, name='artist_delete'),
# Locations
path('locations/', views.location_index, name='location_index'),
path('location/<int:location_id>/', views.location_show, name='location_show'),

# Localities
path('localities/', views.locality_index, name='locality_index'),

]