from django.urls import path 
from . import views 

app_name = 'catalogue' 

urlpatterns = [ 
    path('artists/', views.index, name='artist_index'), 
    path('shows/', views.show_index, name='show_index'), 
    path('shows/<int:show_id>/', views.show_detail, name='show_detail'), 
    # CETTE LIGNE MANQUAIT OU ÉTAIT MAL NOMMÉE :
    path('shows/<slug:slug>/representations/', views.show_representations, name='show_representations'),
    path('signup/', views.signup, name='signup'), 
    path('book/<int:representation_id>/', views.book_representation, name='book_representation'),
   path('', views.welcome, name='welcome'),
]