from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import Artist, Show, Representation
from .forms import SignUpForm

from django.contrib.auth.decorators import login_required

@login_required # Redirige vers login si l'utilisateur n'est pas connecté
def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, pk=representation_id)
    # ... reste de ton code ...

def index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/index.html', {'artists': artists, 'resource': 'artistes'})

def show_index(request):
    shows = Show.objects.all()
    return render(request, 'catalogue/show_index.html', {'shows': shows})

def show_detail(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # Hashage obligatoire 
            user.save()
            return redirect('login') # Redirection vers connexion 
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, pk=representation_id)
    if request.method == 'POST':
        places = request.POST.get('places')
        return render(request, 'catalogue/reservation_confirm.html', {
            'places': places,
            'representation': representation
        })
    return render(request, 'catalogue/book.html', {'representation': representation})

def show_representations(request, slug):
    show = get_object_or_404(Show, slug=slug)
    representations = show.representations.all()
    return render(request, 'catalogue/show_representations.html', {
        'show': show,
        'representations': representations
    })