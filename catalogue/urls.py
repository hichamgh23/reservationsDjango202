from django.urls import path 
from . import views 
from api.catalogue.views import ArtistListCreateView, ArtistRetrieveUpdateDestroyView 
 
app_name='catalogue' 
 
urlpatterns = [ 
    path('artists/', views.index, name='artist_index'), 
    path('shows/', views.show_index, name='show_index'), 
    path('shows/<int:show_id>/', views.show_detail, name='show_detail'), 
    path('api/artists/', ArtistListCreateView.as_view(), name='artist-list'), 
    path('api/artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'), 
    path('register/', views.register, name='register'),
    path('show/<slug:slug>/representations/', views.show_representations, name='show_representations'),
    path('book/<int:representation_id>/', views.book_representation, name='book_representation'),
] 
