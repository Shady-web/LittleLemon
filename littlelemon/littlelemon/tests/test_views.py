from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from restaurant.models import MenuItem
from restaurant.serializers import MenuItemSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class MenuItemViewTest(TestCase):
    def setUp(self):
        # Create a user and get the token, make sure to use APIClient to simulate the request process
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        #Create a few test instances of the Menu model before each test.
        self.menu1 = MenuItem.objects.create(title="Lemonade", price=8.5, inventory=5)
        self.menu2 = MenuItem.objects.create(title="Strawberry", price=9.5, inventory=50)
        self.menu3 = MenuItem.objects.create(title="Milkshake", price=4.5, inventory=30)

    def test_getall(self):
        """
        Test that the view retrieves and serializes all Menu objects.
        """
        response = self.client.get('/restaurant/menu-items/') #ensure the ul path is correct
        menus = MenuItem.objects.all()
        serializer = MenuItemSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) #This ensures returned data and the serialized data matches