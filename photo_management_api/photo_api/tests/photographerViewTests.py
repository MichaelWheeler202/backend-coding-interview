from django.contrib.auth.models import User
from django.test import TestCase, Client

from ..models import Photographer


class PhotographerViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        Photographer.objects.create(id=1, photographer='Felix', photographer_url='http://example.com')

    def tearDown(self):
        self.client.logout()

    def test_get_photographer_retrieves_photographer(self):
        response = self.client.get('/photo_api/photographers/1/')
        self.assertEqual(response.status_code, 200)
        responsePhotographer = response.json()

        # validate all 3 fields in response
        self.assertEqual(1, responsePhotographer["id"])
        self.assertEqual("Felix", responsePhotographer["photographer"])
        self.assertEqual("http://example.com", responsePhotographer["photographer_url"])

    def test_get_photographer_cant_find_photographer(self):
        response = self.client.get('/photo_api/photographers/9999/')
        self.assertEqual(response.status_code, 404)
        responseData = response.json()
        self.assertEqual("Photographer ID 9999 not found.", responseData["error"])

    def test_get_photographer_invalid_id(self):
        response = self.client.get('/photo_api/photographers/0/')
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertEqual("Positive Integer for ID is required.", responseData["error"])


    def test_create_photographer_missing_required_fields(self):
        response = self.client.post('/photo_api/photographers/', {})
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertIn("This field is required.", responseData["id"])
        self.assertIn("This field is required.", responseData["photographer"])


    def test_create_photographer_with_taken_id(self):
        response = self.client.post('/photo_api/photographers/', {
            "id": 1,
            "photographer": "Felix",
            "photographer_url": "http://valid-url.com"
        })
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertIn("photographer with this id already exists.", responseData["id"])

    def test_create_photographer_invalid_field_values(self):
        response = self.client.post('/photo_api/photographers/', {
            "id": 2,
            "photographer": "Marcus",
            "photographer_url": "not-a-valid-url"
        })
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertIn("Enter a valid URL.", responseData["photographer_url"])

    def test_create_photographer_valid(self):
        response = self.client.post('/photo_api/photographers/', {
            "id": 2,
            "photographer": "Marcus",
            "photographer_url": "http://valid-url.com"
        })
        self.assertEqual(response.status_code, 201)
        get_response = self.client.get('/photo_api/photographers/2/')
        self.assertEqual(get_response.status_code, 200)
        responsePhotographer = get_response.json()
        self.assertEqual(2, responsePhotographer["id"])
        self.assertEqual("Marcus", responsePhotographer["photographer"])
        self.assertEqual("http://valid-url.com", responsePhotographer["photographer_url"])


    def test_delete_photographer_deletes_a_photographer_and_all_their_pictures(self):
        photographer_id = 3
        # create photographer to delete
        response = self.client.post('/photo_api/photographers/', {
            "id": photographer_id,
            "photographer": "Mart",
            "photographer_url": "http://valid-url.com"
        })
        self.assertEqual(response.status_code, 201)

        # confirm photographer created
        get_response = self.client.get(f'/photo_api/photographers/{photographer_id}/')
        self.assertEqual(get_response.status_code, 200)
        responsePhotographer = get_response.json()
        self.assertEqual(photographer_id, responsePhotographer["id"])
        self.assertEqual("Mart", responsePhotographer["photographer"])
        self.assertEqual("http://valid-url.com", responsePhotographer["photographer_url"])

        # create first photo for photographer
        response = self.client.post('/photo_api/photos/', {
            "id": 12345,
            "photographer_id": photographer_id,
            "width": 5284,
            "height": 3514,
            "url": "https://www.pexels.com/photo/elderly-man-and-woman-with-bikes-at-park-21405575/",
            "avg_color": "#6D755E",
            "src_original": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg",
            "src_large2x": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            "src_large": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
            "src_medium": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&h=350",
            "src_small": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&h=130",
            "src_portrait": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800",
            "src_landscape": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200",
            "src_tiny": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280",
            "alt": "Two older people cycling"
        })
        self.assertEqual(response.status_code, 201)

        # create second photo for photographer
        response = self.client.post('/photo_api/photos/', {
            "id": 12346,
            "photographer_id": photographer_id,
            "width": 5284,
            "height": 3514,
            "url": "https://www.pexels.com/photo/elderly-man-and-woman-with-bikes-at-park-21405575/",
            "avg_color": "#6D755E",
            "src_original": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg",
            "src_large2x": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            "src_large": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
            "src_medium": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&h=350",
            "src_small": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&h=130",
            "src_portrait": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800",
            "src_landscape": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200",
            "src_tiny": "https://images.pexels.com/photos/21405575/pexels-photo-21405575.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280",
            "alt": "Two older people cycling"
        })
        self.assertEqual(response.status_code, 201)

        # confirm photos created
        get_response = self.client.get('/photo_api/photos/12345/')
        self.assertEqual(get_response.status_code, 200)
        get_response = self.client.get('/photo_api/photos/12346/')
        self.assertEqual(get_response.status_code, 200)

        # delete photographer
        response = self.client.delete(f'/photo_api/photographers/{photographer_id}/')
        self.assertEqual(response.status_code, 200)

        # confirm photographer deleted
        get_response = self.client.get(f'/photo_api/photographers/{photographer_id}/')
        self.assertEqual(get_response.status_code, 404)

        # confirm photos deleted
        get_response = self.client.get('/photo_api/photos/12345/')
        self.assertEqual(get_response.status_code, 404)
        get_response = self.client.get('/photo_api/photos/12346/')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_photographer_cant_find_photographer(self):
        response = self.client.delete('/photo_api/photographers/9999/')
        self.assertEqual(response.status_code, 404)
        responseData = response.json()
        self.assertEqual("Photographer ID 9999 not found.", responseData["error"])

    def test_delete_photographer_invalid_id(self):
        response = self.client.delete('/photo_api/photographers/0/')
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertEqual("Positive Integer for ID is required.",responseData["error"])
