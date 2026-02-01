from django.contrib.auth.models import User
from django.test import TestCase, Client

from ..models import Photo, Photographer


class PhotoViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.client.login(username='testuser2', password='testpass123')

        # create a Photographer to satisfy Photo foreign key requirements
        photographer = Photographer.objects.create(id=1, photographer='Felix', photographer_url='http://example.com')

        # create an initial Photo
        Photo.objects.create(
            id=21751820,
            photographer_id=photographer,
            width = 3888,
            height = 5184,
            url = 'https://www.pexels.com/photo/a-small-island-surrounded-by-trees-in-the-middle-of-a-lake-21751820/',
            avg_color = '#333831',
            src_original = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg',
            src_large2x = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            src_large = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
            src_medium = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&h=350',
            src_small = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&h=130',
            src_portrait = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800',
            src_landscape = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200',
            src_tiny = 'https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280',
            alt = 'A small island surrounded by trees in the middle of a lake'
        )

    def tearDown(self):
        self.client.logout()

    def test_get_photo_retrieves_photo(self):
        response = self.client.get('/photo_api/photos/21751820/')
        self.assertEqual(response.status_code, 200)
        responseData = response.json()

        # validate at least id and url are present
        self.assertEqual(21751820, responseData["id"])
        self.assertEqual(1, responseData["photographer_id"])
        self.assertEqual(3888, responseData["width"])
        self.assertEqual(5184, responseData["height"])
        self.assertEqual('https://www.pexels.com/photo/a-small-island-surrounded-by-trees-in-the-middle-of-a-lake-21751820/', responseData["url"])
        self.assertEqual('#333831', responseData["avg_color"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg', responseData["src_original"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', responseData["src_large2x"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', responseData["src_large"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&h=350', responseData["src_medium"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&h=130', responseData["src_small"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', responseData["src_portrait"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200',  responseData["src_landscape"])
        self.assertEqual('https://images.pexels.com/photos/21751820/pexels-photo-21751820.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280', responseData["src_tiny"])
        self.assertEqual('A small island surrounded by trees in the middle of a lake', responseData["alt"])


    def test_get_photo_cant_find_photo(self):
        response = self.client.get('/photo_api/photos/9999/')
        self.assertEqual(response.status_code, 404)
        responseData = response.json()
        self.assertEqual("Photo ID 9999 does not exist.", responseData["error"])

    def test_get_photo_invalid_id(self):
        response = self.client.get('/photo_api/photos/0/')
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertEqual("Positive Integer for ID is required.", responseData["error"])


    def test_create_photo_missing_required_fields(self):
        response = self.client.post('/photo_api/photos/', {})
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        # at least one required field should be reported missing
        self.assertIn("This field is required.", responseData["id"])
        self.assertIn("This field is required.", responseData["url"])
        self.assertIn("This field is required.", responseData["src_original"])


    def test_create_photo_with_taken_id(self):
        response = self.client.post('/photo_api/photos/', {
            "id": 21751820,
            "photographer_id": 1,
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
        # duplicate id should result in a client error (400)
        self.assertEqual(response.status_code, 400)

    def test_create_photo_invalid_field_values(self):
        response = self.client.post('/photo_api/photos/', {
            "id": 21405575,
            "photographer_id": 1,
            "width": 5284,
            "height": 3514,
            "url": "invalid_url",
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
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertIn("Enter a valid URL.", responseData["url"])

    def test_create_photo_valid(self):
        response = self.client.post('/photo_api/photos/', {
            "id": 21405575,
            "photographer_id": 1,
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
        get_response = self.client.get('/photo_api/photos/21405575/')
        self.assertEqual(get_response.status_code, 200)

    def test_delete_photo_deletes_a_photo(self):
        photo_id = 123
        # create photo to delete
        response = self.client.post('/photo_api/photos/', {
            "id": photo_id,
            "photographer_id": 1,
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

        # confirm photo created
        get_response = self.client.get(f'/photo_api/photos/{photo_id}/')
        self.assertEqual(get_response.status_code, 200)
        data = get_response.json()
        self.assertEqual(photo_id, data.get("id"))

        # delete photo
        response = self.client.delete(f'/photo_api/photos/{photo_id}/')
        self.assertEqual(response.status_code, 200)

        # confirm photo deleted
        get_response = self.client.get(f'/photo_api/photos/{photo_id}/')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_photo_cant_find_photo(self):
        response = self.client.delete('/photo_api/photos/9999/')
        self.assertEqual(response.status_code, 404)
        responseData = response.json()
        self.assertEqual("Photo ID 9999 does not exist.", responseData["error"])

    def test_delete_photo_invalid_id(self):
        response = self.client.delete('/photo_api/photos/0/')
        self.assertEqual(response.status_code, 400)
        responseData = response.json()
        self.assertEqual("Positive Integer for ID is required.", responseData["error"])
