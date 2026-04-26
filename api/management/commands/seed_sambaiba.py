"""
Populate demo data for community tables.

Removes any rows previously created by this command (title/name starting with "[Seed] ")
and inserts fresh samples. Safe to re-run.

The existing Django admin user (e.g. username "admin") is not modified; content models
do not require a foreign key to User.
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.contacts.models import UsefulContact
from apps.event_categories.models import EventCategory
from apps.gallery_categories.models import GalleryCategory
from apps.collection_points.models import CollectionPoint
from apps.donations.models import DonationCampaign, DonationCampaignPointLink
from apps.events.models import CommunityEvent
from apps.gallery.models import GalleryItem
from apps.news.models import CommunityNews
from apps.suggestions.models import CommunitySuggestion

SEED_PREFIX = "[Seed] "


class Command(BaseCommand):
    help = "Populate community tables with demo rows (idempotent via [Seed] prefix)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-suggestions",
            action="store_true",
            help="Do not create sample suggestions.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        admins = User.objects.filter(is_superuser=True)
        if admins.exists():
            self.stdout.write(
                self.style.SUCCESS(
                    f"Found {admins.count()} superuser(s); first: {admins.first().username!r}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "No superuser found. Create one with: python manage.py createsuperuser"
                )
            )

        self._clear_seed_rows()
        self._seed_events()
        self._seed_gallery()
        self._seed_donations()
        self._seed_news()
        self._seed_contacts()
        if not options["skip_suggestions"]:
            self._seed_suggestions()

        self.stdout.write(self.style.SUCCESS("Seed completed successfully."))

    def _clear_seed_rows(self):
        n_e = CommunityEvent.objects.filter(title__startswith=SEED_PREFIX).delete()[0]
        n_g = GalleryItem.objects.filter(title__startswith=SEED_PREFIX).delete()[0]
        seed_campaign_ids = list(
            DonationCampaign.objects.filter(title__startswith=SEED_PREFIX).values_list("id", flat=True)
        )
        seed_point_ids = set(
            DonationCampaignPointLink.objects.filter(campaign_id__in=seed_campaign_ids).values_list(
                "collection_point_id", flat=True
            )
        )
        n_d = DonationCampaign.objects.filter(title__startswith=SEED_PREFIX).delete()[0]
        n_pt = 0
        for pid in seed_point_ids:
            if not DonationCampaignPointLink.objects.filter(collection_point_id=pid).exists():
                n_pt += CollectionPoint.objects.filter(pk=pid).delete()[0]
        n_n = CommunityNews.objects.filter(title__startswith=SEED_PREFIX).delete()[0]
        n_c = UsefulContact.objects.filter(name__startswith=SEED_PREFIX).delete()[0]
        n_s = CommunitySuggestion.objects.filter(name__startswith=SEED_PREFIX).delete()[0]
        self.stdout.write(
            f"Removed previous seed rows: events={n_e}, gallery={n_g}, "
            f"donations={n_d}, donation_points={n_pt}, news={n_n}, contacts={n_c}, suggestions={n_s}"
        )

    def _seed_events(self):
        today = date.today()
        c = {s: EventCategory.objects.get(slug=s) for s in EventCategory.objects.values_list("slug", flat=True)}
        rows = [
            CommunityEvent(
                title=f"{SEED_PREFIX}Vacinação no CRAS",
                description="Campanha de vacinação influenza para idosos.",
                date=today + timedelta(days=5),
                time="08:00–12:00",
                location="CRAS – Centro",
                category=c["saude"],
                is_highlighted=True,
            ),
            CommunityEvent(
                title=f"{SEED_PREFIX}Reunião de moradores",
                description="Pauta: iluminação pública e coleta seletiva.",
                date=today + timedelta(days=12),
                time="19:00",
                location="Praça Central",
                category=c["cultura"],
                is_highlighted=False,
            ),
            CommunityEvent(
                title=f"{SEED_PREFIX}Aulão de reforço escolar",
                description="Matemática e português para ensino fundamental.",
                date=today + timedelta(days=20),
                time="14:00–17:00",
                location="Escola Municipal",
                category=c["educacao"],
                is_highlighted=True,
            ),
            CommunityEvent(
                title=f"{SEED_PREFIX}Feira do comércio local",
                description="Produtos da agricultura familiar.",
                date=today + timedelta(days=28),
                time="07:00–13:00",
                location="Av. Principal",
                category=c["comercio"],
                is_highlighted=False,
            ),
            CommunityEvent(
                title=f"{SEED_PREFIX}Dia do trabalhador (comemoração)",
                description="Apresentações culturais e food trucks.",
                date=date(today.year, 5, 1),
                time="10:00",
                location="Praça Central",
                category=c["data_comemorativa"],
                is_highlighted=True,
            ),
        ]
        CommunityEvent.objects.bulk_create(rows)
        self.stdout.write(f"Created {len(rows)} events.")

    def _seed_gallery(self):
        c = {s: GalleryCategory.objects.get(slug=s) for s in GalleryCategory.objects.values_list("slug", flat=True)}
        rows = [
            GalleryItem(
                title=f"{SEED_PREFIX}Ação de limpeza",
                category=c["eventos"],
                media_type=GalleryItem.MediaType.IMAGE,
                media_url="https://picsum.photos/seed/sambaiba1/800/600",
            ),
            GalleryItem(
                title=f"{SEED_PREFIX}Entrega de cestas",
                category=c["campanhas"],
                media_type=GalleryItem.MediaType.IMAGE,
                media_url="https://picsum.photos/seed/sambaiba2/800/600",
            ),
            GalleryItem(
                title=f"{SEED_PREFIX}Oficina de arte",
                category=c["cultura"],
                media_type=GalleryItem.MediaType.IMAGE,
                media_url="https://picsum.photos/seed/sambaiba3/800/600",
            ),
            GalleryItem(
                title=f"{SEED_PREFIX}Palestra de saúde",
                category=c["saude"],
                media_type=GalleryItem.MediaType.IMAGE,
                media_url="https://picsum.photos/seed/sambaiba4/800/600",
            ),
        ]
        GalleryItem.objects.bulk_create(rows)
        self.stdout.write(f"Created {len(rows)} gallery items.")

    def _seed_donations(self):
        c1 = DonationCampaign.objects.create(
            title=f"{SEED_PREFIX}Campanha do agasalho",
            description="Arrecadação de roupas de frio em bom estado.",
            donation_type=DonationCampaign.DonationType.ROUPAS,
            is_active=True,
            goal_target=500,
            goal_unit="peças",
        )
        c2 = DonationCampaign.objects.create(
            title=f"{SEED_PREFIX}Banco de alimentos",
            description="Alimentos não perecíveis para cestas básicas.",
            donation_type=DonationCampaign.DonationType.ALIMENTOS,
            is_active=True,
            goal_target=200,
            goal_unit="cestas",
        )
        c3 = DonationCampaign.objects.create(
            title=f"{SEED_PREFIX}Campanha encerrada (exemplo)",
            description="Exemplo de campanha inativa (sem meta numérica no seed).",
            donation_type=DonationCampaign.DonationType.BRINQUEDOS,
            is_active=False,
            goal_target=None,
            goal_unit="",
        )
        p1 = CollectionPoint.objects.create(
            name="Associação de Moradores",
            address="Praça Central, s/n",
            hours="Seg–Sex, 8h–12h",
        )
        p2 = CollectionPoint.objects.create(
            name="Escola Municipal",
            address="Rua da Educação, 789",
            hours="Seg–Sex, 7h–17h",
        )
        p3 = CollectionPoint.objects.create(
            name="CRAS",
            address="Av. Principal, 456",
            hours="Seg–Sex, 8h–16h",
        )
        DonationCampaignPointLink.objects.bulk_create(
            [
                DonationCampaignPointLink(campaign=c1, collection_point=p1, sort_order=0),
                DonationCampaignPointLink(campaign=c1, collection_point=p2, sort_order=1),
                DonationCampaignPointLink(campaign=c2, collection_point=p3, sort_order=0),
            ]
        )
        self.stdout.write("Created 3 donation campaigns, 3 global collection points, and 3 links.")

    def _seed_news(self):
        rows = [
            CommunityNews(
                title=f"{SEED_PREFIX}Horário especial no posto",
                content="Na próxima semana o posto funcionará em horário estendido das 7h às 19h.",
                category=CommunityNews.NewsCategory.AVISO,
                is_pinned=True,
            ),
            CommunityNews(
                title=f"{SEED_PREFIX}Mutirão de pintura",
                content="Inscrições abertas para voluntários no CRAS até sexta-feira.",
                category=CommunityNews.NewsCategory.COMUNICADO,
                is_pinned=False,
            ),
            CommunityNews(
                title=f"{SEED_PREFIX}Atualização do calendário escolar",
                content="Recesso antecipado conforme calendário municipal publicado no diário oficial.",
                category=CommunityNews.NewsCategory.ATUALIZACAO,
                is_pinned=False,
            ),
        ]
        CommunityNews.objects.bulk_create(rows)
        self.stdout.write(f"Created {len(rows)} news items.")

    def _seed_contacts(self):
        rows = [
            UsefulContact(
                name=f"{SEED_PREFIX}Posto de Saúde Central",
                phone="(86) 3215-0000",
                address="Rua da Saúde, 123 – Centro",
                hours="Mon–Fri, 7am–5pm",
                sort_order=10,
                is_published=True,
            ),
            UsefulContact(
                name=f"{SEED_PREFIX}CRAS",
                phone="(86) 3215-1111",
                address="Av. Principal, 456",
                hours="Mon–Fri, 8am–4pm",
                sort_order=20,
                is_published=True,
            ),
            UsefulContact(
                name=f"{SEED_PREFIX}Defesa Civil",
                phone="199",
                address="24h",
                hours="24 hours",
                sort_order=30,
                is_published=True,
            ),
            UsefulContact(
                name=f"{SEED_PREFIX}Rascunho (não publicado)",
                phone="(86) 0000-0000",
                address="Internal only",
                hours="N/A",
                sort_order=99,
                is_published=False,
            ),
        ]
        UsefulContact.objects.bulk_create(rows)
        self.stdout.write(f"Created {len(rows)} contacts.")

    def _seed_suggestions(self):
        rows = [
            CommunitySuggestion(
                name=f"{SEED_PREFIX}Maria Silva",
                email="maria.example@email.com",
                suggestion_type=CommunitySuggestion.SuggestionType.EVENTO,
                message="Sugestão de feira de trocas no próximo mês.",
                reviewed=False,
            ),
            CommunitySuggestion(
                name=f"{SEED_PREFIX}João",
                email="",
                suggestion_type=CommunitySuggestion.SuggestionType.INFORMACAO,
                message="Informar que a rua X está sem iluminação.",
                reviewed=True,
            ),
        ]
        CommunitySuggestion.objects.bulk_create(rows)
        self.stdout.write(f"Created {len(rows)} suggestions.")
