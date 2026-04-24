from django.urls import path
from . import views

urlpatterns = [
    path('artists/', views.ArtistListCreateView.as_view(), name='artist-list'),
    path('artists/<int:pk>/', views.ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),
]