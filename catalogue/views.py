from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Artist, Show, Representation, Reservation
from .forms import RegistrationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

# --- ARTISTES ---

def index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/index.html', {'artists': artists})

# --- SPECTACLES ---

def show_index(request):
    """Affiche la liste des spectacles (Image 1 du document)"""
    shows = Show.objects.all()
    return render(request, 'catalogue/show_index.html', {'shows': shows})

def show_detail(request, show_id):
    """Affiche le détail d'un spectacle"""
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

# --- AUTHENTIFICATION ---

def register(request):
    """Gère l'inscription des nouveaux membres"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- PROCESSUS DE RÉSERVATION (CHAPITRE 10) ---

def show_representations(request, slug):
    """Étape 1 : Choisir une date (Image 2 du document)"""
    show = get_object_or_404(Show, slug=slug)
    representations = show.representations.all()
    return render(request, 'catalogue/show_representations.html', {
        'show': show, 
        'representations': representations
    })

@login_required
def book_representation(request, representation_id):
    """Étape 2 : Choisir le nombre de places (Image 3 du document)"""
    representation = get_object_or_404(Representation, id=representation_id)
    
    if request.method == 'POST':
        places = request.POST.get('places')
        if places and int(places) > 0:
            # Création de la réservation liée à l'utilisateur connecté
            Reservation.objects.create(
                user=request.user,
                representation=representation,
                places=int(places)
            )
            # Rediriger vers la confirmation ou le panier (Image 5)
            return render(request, 'catalogue/reservation_confirm.html', {
                'representation': representation,
                'places': places
            })

    return render(request, 'catalogue/book_places.html', {
        'representation': representation
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) # Hashage du mot de passe 
            user.save()
            return redirect('login') # Redirection vers la connexion 
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})