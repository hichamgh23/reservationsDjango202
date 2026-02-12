from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Artist, Show, Representation
from .forms import SignUpForm

# --- PAGE D'ACCUEIL ---
def welcome(request):
    """Affiche la page d'accueil avec les 3 derniers spectacles."""
    latest_shows = Show.objects.all().order_by('-id')[:3]
    return render(request, 'catalogue/welcome.html', {
        'latest_shows': latest_shows
    })

# --- ARTISTES ---
def index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/index.html', {'artists': artists, 'resource': 'artistes'})

# --- SPECTACLES ---
def show_index(request):
    shows = Show.objects.all()
    return render(request, 'catalogue/show_index.html', {'shows': shows})

def show_detail(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

def show_representations(request, slug):
    show = get_object_or_404(Show, slug=slug)
    representations = show.representations.all()
    return render(request, 'catalogue/show_representations.html', {
        'show': show,
        'representations': representations
    })

# --- AUTHENTIFICATION ---
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # Hashage du mot de passe
            user.save()
            return redirect('login') 
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- RÉSERVATION ---
@login_required
def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, pk=representation_id)
    
    if request.method == 'POST':
        # On récupère le nombre de places depuis le formulaire
        places = request.POST.get('places', 1)
        
        # On renvoie vers la page de confirmation
        return render(request, 'catalogue/reservation_confirm.html', {
            'representation': representation,
            'places': places,
            'user': request.user
        })
    
    # Formulaire de choix du nombre de places
    return render(request, 'catalogue/book.html', {'representation': representation})