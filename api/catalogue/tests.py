from django.urls import reverse 
from rest_framework import status 
from rest_framework.test import APITestCase 
from catalogue.models import Artist 
from django.contrib.auth.models import User 
 
class ArtistAPITests(APITestCase): 
    def setUp(self): 
        self.user = User.objects.create_superuser(username='testadmin', password='password123') 
        self.artist = Artist.objects.create(firstname="Daniel", lastname="Marcelin") 
 
    def test_get_artist_list(self): 
        self.client.login(username='testadmin', password='password123') 
        url = reverse('catalogue:artist-list') 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
