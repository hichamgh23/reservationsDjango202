from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from catalogue import views as catalogue_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accueil -> Spectacles
    path('', RedirectView.as_view(url='/shows/', permanent=True)),
    path('', include('catalogue.urls')),
    # Les routes d'authentification de Django (login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')), 
    path('signup/', catalogue_views.signup, name='signup'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
