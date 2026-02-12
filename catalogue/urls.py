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

    # Processus de réservation (Le nom utilisé dans le HTML ci-dessus)
    path('book/<int:representation_id>/', views.book_representation, name='book_representation'),
]