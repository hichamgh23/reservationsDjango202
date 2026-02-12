from django.contrib import admin
from django.urls import path, include
from catalogue import views as catalogue_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CETTE LIGNE EST LA PRIORITÉ NUMÉRO 1
    path('', catalogue_views.welcome, name='home'), 
    
    # On inclut le reste SANS préfixe pour que 'shows/' reste accessible
    path('', include('catalogue.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')), 
]
