from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

from main.models import Experience, Education, PreviousWork


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
        title="Asisten Dosen PBP",
        description="Membantu mahasiswa memahami pengembangan web.",
        category="part-time",
        started_at=timezone.make_aware(datetime(2026, 1, 1)),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="grid"')

        api_response = self.client.get(
            reverse("api:experience-list")
        )

        self.assertEqual(api_response.status_code, 200)

        data = api_response.json()

        experience_data = next(
            item for item in data
            if item["id"] == str(self.experience.id)
        )

        self.assertEqual(
            experience_data["title"],
            self.experience.title
        )
        
    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada experience yang ditambahkan")

    def test_completed_experience(self):
        completed_experience = Experience.objects.create(
            title="Web Developer Intern",
            description="Mengembangkan website.",
            category="internship",
            started_at=timezone.make_aware(datetime(2025, 1, 1)),
            ended_at=timezone.make_aware(datetime(2025, 6, 1)),
        )

        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="grid"')

        api_response = self.client.get(
            reverse("api:experience-list")
        )

        self.assertEqual(api_response.status_code, 200)

        data = api_response.json()

        experience_data = next(
            item for item in data
            if item["id"] == str(completed_experience.id)
        )

        self.assertFalse(experience_data["is_ongoing"])

        
class PreviousWorkTest(TestCase):
    def test_previous_work_url_and_template(self):
        response = self.client.get(
            reverse("main:show_previous_work")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "PreviousWork.html"
        )

    def test_previous_work_data_appears_on_page(self):
        previous_work = PreviousWork.objects.create(
            title="Website Wali",
            role="Project Manager",
            description="Mengelola pengembangan website Wali.",
            date="2026-04-01",
            category="Web Development",
            link="https://example.com",
        )

        response = self.client.get(
            reverse("main:show_previous_work")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="previous-work-grid"')

        api_response = self.client.get(
            reverse("api:project-list")
        )

        self.assertEqual(api_response.status_code, 200)

        data = api_response.json()

        previous_work_data = next(
            item for item in data
            if item["id"] == previous_work.id
        )

        self.assertEqual(
            previous_work_data["title"],
            previous_work.title
        )
        self.assertEqual(
            previous_work_data["role"],
            previous_work.role
        )
        self.assertEqual(
            previous_work_data["description"],
            previous_work.description
        )
        self.assertEqual(
            previous_work_data["category"],
            previous_work.category
        )

    def test_empty_previous_work_page(self):
        response = self.client.get(
            reverse("main:show_previous_work")
        )

        self.assertContains(
            response,
            "Belum ada previous work yang ditambahkan"
        )