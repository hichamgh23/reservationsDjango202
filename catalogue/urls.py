from django.urls import path
from . import views

urlpatterns = [
    path('artists/', views.index, name='artist_index'),
]
urlpatterns = [
    path('artists/', views.index, name='artist_index'),
    path('shows/', views.show_index, name='show_index'), # Nouvelle ligne
]
urlpatterns = [
    path('artists/', views.index, name='artist_index'),
    path('shows/', views.show_index, name='show_index'),
    path('shows/<int:show_id>/', views.show_detail, name='show_detail'), # Nouvelle ligne
]