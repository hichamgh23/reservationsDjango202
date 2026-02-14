from django.contrib import admin
from django.urls import path, include
from catalogue import views as catalogue_views 
from django.conf import settings # AJOUT : Pour accéder à MEDIA_URL
from django.conf.urls.static import static # AJOUT : Pour servir les fichiers

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

# AJOUT CHIRURGICAL : Activation de l'accès aux images dans le navigateur
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
