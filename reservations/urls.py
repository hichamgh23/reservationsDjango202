from django.contrib import admin
from django.urls import path, include
from catalogue import views as catalogue_views 
from django.conf import settings 
from django.conf.urls.static import static 
from django.views.decorators.csrf import csrf_exempt # AJOUT DE SÉCURITÉ

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Priorité 1 : Accueil
    path('', catalogue_views.welcome, name='welcome'), 
    
    # Inscription
    path('signup/', catalogue_views.signup, name='signup'), 
    
    # LA SOLUTION FINALE : On rend la vue de déconnexion insensible aux restrictions
    path('accounts/logout/', csrf_exempt(catalogue_views.logout_user), name='logout'),
    
    # Authentification Django
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Inclusion des urls de l'app catalogue
    path('', include('catalogue.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
