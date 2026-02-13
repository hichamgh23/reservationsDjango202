from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Show, Representation, Reservation

# 1. Page d'accueil
def welcome(request):
    return render(request, 'catalogue/welcome.html', {'user': request.user})

# 2. Inscription
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Inscription réussie ! Veuillez vous connecter.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# 3. Catalogue des spectacles
def show_index(request):
    # Récupération des spectacles triés par titre
    shows = Show.objects.all().order_by('title')
    return render(request, 'catalogue/show_index.html', {
        'shows': shows, 
        'titre': 'Liste des spectacles'
    })

# 4. Détail du spectacle
def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'catalogue/show_detail.html', {'show': show})

# 5. Réservation
@login_required
def book_representation(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    
    if request.method == 'POST':
        try:
            places = int(request.POST.get('places', 1))
            if places < 1:
                raise ValueError
                
            Reservation.objects.create(
                user=request.user, 
                representation=representation, 
                places=places
            )
            
            total_price = places * representation.show.price
            
            return render(request, 'catalogue/reservation_confirm.html', {
                'representation': representation,
                'places': places,
                'total_price': total_price
            })
        except ValueError:
            messages.error(request, "Veuillez entrer un nombre de places valide.")
            
    return render(request, 'catalogue/book.html', {'representation': representation})