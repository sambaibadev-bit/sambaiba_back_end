from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.news.models import CommunityNews


class NewsDateTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="admin-news",
            password="secret",
            role="admin",
        )
        self.client.force_authenticate(user)

    def test_patch_updates_news_date(self):
        item = CommunityNews.objects.create(
            title="Aviso",
            summary="Resumo",
            content="Conteúdo",
        )
        published = timezone.now() - timedelta(days=12)
        response = self.client.patch(
            f"/api/community/news/{item.pk}/",
            {"created_date": published.isoformat()},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertAlmostEqual(item.created_at.timestamp(), published.timestamp(), delta=1)

    def test_create_accepts_news_date(self):
        published = timezone.now() - timedelta(days=3)
        response = self.client.post(
            "/api/community/news/",
            {
                "title": "Comunicado",
                "summary": "Resumo",
                "content": "Conteúdo",
                "category": "comunicado",
                "created_date": published.isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        item = CommunityNews.objects.get(pk=response.data["id"])
        self.assertAlmostEqual(item.created_at.timestamp(), published.timestamp(), delta=1)
