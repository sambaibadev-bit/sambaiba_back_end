import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.test import APITestCase

from apps.event_categories.models import EventCategory
from apps.events.models import CommunityEvent


def tiny_png():
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), "red").save(buffer, format="PNG")
    return SimpleUploadedFile("lugar.png", buffer.getvalue(), content_type="image/png")


class EventImageTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="admin-events",
            password="secret",
            role="admin",
        )
        self.client.force_authenticate(user)
        self.category, _created = EventCategory.objects.get_or_create(
            slug="cultura",
            defaults={"name": "Cultura"},
        )

    def test_create_event_with_place_image(self):
        response = self.client.post(
            "/api/community/events/",
            {
                "title": "Vacinação",
                "description": "Atendimento no posto.",
                "date": "2026-11-02",
                "location": "Posto Central",
                "category_id": self.category.pk,
                "image": tiny_png(),
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(response.data["image"])
        item = CommunityEvent.objects.get(pk=response.data["id"])
        self.assertTrue(item.image.name.startswith("events/"))
