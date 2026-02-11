from django.shortcuts import render, get_object_or_404
from .models import Artist
from .models import Show  

def index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/index.html', {'artists': artists})



def show_index(request):
    shows = Show.objects.all()
    return render(request, 'catalogue/show_index.html', {'shows': shows})

def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})