from django.contrib import admin
from django.urls import path, include
from catalogue import views as catalogue_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Priorité 1 : Accueil
    path('', catalogue_views.welcome, name='welcome'), 
    
    # LA LIGNE MANQUANTE : Sans elle, le bouton Inscription fait crash le site
    path('signup/', catalogue_views.signup, name='signup'), 
    
    # Inclusion des urls de l'app catalogue
    path('', include('catalogue.urls')),
    
    # Authentification Django (Login/Logout)
    path('accounts/', include('django.contrib.auth.urls')), 
]
