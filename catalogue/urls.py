from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    # Liste des artistes
    path('artists/', views.index, name='artist_index'),
    
    # Liste des spectacles
    path('shows/', views.show_index, name='show_index'),
    
    # Détail d'un spectacle (ex: /shows/5/)
    path('shows/<int:show_id>/', views.show_detail, name='show_detail'),
]
