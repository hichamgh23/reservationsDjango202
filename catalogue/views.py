from django.shortcuts import render, get_object_or_404
from .models import Artist, Show

# Vue pour la liste des artistes
def index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/index.html', {'artists': artists})

# Vue pour la liste des spectacles (Chapitre 9)
def show_index(request):
    shows = Show.objects.all()
    return render(request, 'catalogue/show_index.html', {'shows': shows})

# Vue pour le détail d'un spectacle (Page individuelle)
def show_detail(request, show_id):
    # On récupère le spectacle par son ID ou on affiche une erreur 404
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})