
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone
from main.models import PreviousWork, Education, Experience
import uuid
from unittest.mock import patch

class PreviousWorkAPITest(APITestCase):

    def setUp(self):
        # Membuat akun superuser untuk pengujian
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        # Membuat akun biasa
        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        # Membuat data Previous Work awal
        self.previous_work = PreviousWork.objects.create(
        title="Portfolio",
        description="My website",
        role="Developer",
        date="2026-01-01",
        category="Project",
    )

        # URL API
        self.list_url = reverse("api:project-list")

        self.detail_url = reverse(
            "api:project-detail",
            args=[self.previous_work.id],
        )

        self.star_url = reverse(
            "api:project-star",
            args=[self.previous_work.id],
        )

        # Payload sesuai serializer ProjectSerializer
        self.payload = {
        "title": "New Previous Work",
        "description": "A useful project",
        "role": "Developer",
        "date": "2026-01-01",
        "category": "Project",
        "project_url": "https://example.com/",
    }


    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            self.previous_work.id,
        )

        self.assertFalse(
            response.data[0]["is_starred"]
        )

        self.assertNotIn(
            "fields",
            response.data[0],
        )

        detail_response = self.client.get(self.detail_url)

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )


    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "PORT"},
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )

        self.assertEqual(
            response.data,
            [],
        )


    def test_missing_previous_work(self):
        url = reverse(
            "api:project-detail",
            args=[999999],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):

            self.client.force_authenticate(user=user)

            create_response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )

            self.assertEqual(
                create_response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            update_response = self.client.patch(
                self.detail_url,
                {"title": "Changed"},
                format="json",
            )

            self.assertEqual(
                update_response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            delete_response = self.client.delete(
                self.detail_url,
            )

            self.assertEqual(
                delete_response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

        self.assertEqual(
            PreviousWork.objects.count(),
            1,
        )

        self.previous_work.refresh_from_db()

        self.assertEqual(
            self.previous_work.title,
            "Portfolio",
        )


    def test_owner_can_create(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            PreviousWork.objects.filter(
                pk=response.data["id"]
            ).exists()
        )


    def test_validation(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        test_cases = [
            (
                {"title": "   "},
                "title",
            ),
            (
                {"title": '<img src="x" onerror="alert(1)">'},
                "title",
            ),
            (
                {"project_url": "javascript:alert(1)"},
                "project_url",
            ),
        ]

        for changes, field in test_cases:

            response = self.client.post(
                self.list_url,
                {
                    **self.payload,
                    **changes,
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

            self.assertIn(
                field,
                response.data,
            )

        self.assertEqual(
            PreviousWork.objects.count(),
            1,
        )


    @patch.dict("os.environ", {"PORTFOLIO_SECRET": "test-secret"})
    def test_patch_put_and_delete(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        # DELETE
        response = self.client.delete(
            self.detail_url,
            {"secret": "test-secret"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(
            response.content,
            b"",
        )

        self.assertFalse(
            PreviousWork.objects.filter(
                pk=self.previous_work.id
            ).exists()
        )


    def test_star_requires_login_and_toggles(self):

        # Guest tidak boleh memberikan star
        response = self.client.post(
            self.star_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Login sebagai user biasa
        self.client.force_authenticate(
            user=self.visitor,
        )

        # Memberikan star
        response = self.client.post(
            self.star_url,
        )

        self.assertTrue(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["star_count"],
            1,
        )

        # Membatalkan star
        response = self.client.post(
            self.star_url,
        )

        self.assertFalse(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )


    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )

        self.assertFalse(
            response.data["is_starred"]
        )


    def test_editor_can_update_but_cannot_create_or_delete(self):
        editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )

        editor_group, _ = Group.objects.get_or_create(
            name="Editor",
        )

        editor.groups.add(editor_group)

        self.client.force_authenticate(user=editor)

        # Editor boleh PATCH
        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.previous_work.refresh_from_db()

        self.assertEqual(
            self.previous_work.title,
            "Updated by Editor",
        )

        # Editor tidak boleh POST
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Editor tidak boleh DELETE
        response = self.client.delete(
            self.detail_url,
        )

        # Pastikan POST yang ditolak tidak membuat data baru
        self.assertEqual(
            PreviousWork.objects.count(),
            1,
        )

        # Pastikan DELETE yang ditolak tidak menghapus data
        self.assertTrue(
            PreviousWork.objects.filter(
                pk=self.previous_work.id
            ).exists()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_wrong_method(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        response = self.client.delete(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


    def test_session_write_without_csrf_is_rejected(self):

        client = APIClient(
            enforce_csrf_checks=True,
        )

        client.login(
            username="owner",
            password="test-password",
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            PreviousWork.objects.count(),
            1,
        )


    def test_session_write_with_csrf_succeeds(self):

        client = APIClient(
            enforce_csrf_checks=True,
        )

        client.login(
            username="owner",
            password="test-password",
        )

        # Membuka Browsable API untuk memperoleh CSRF token
        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_staff_without_editor_group_cannot_manage_previous_work(self):
        self.visitor.is_staff = True
        self.visitor.save()

        self.client.force_authenticate(
            user=self.visitor,
        )

        response = self.client.patch(
            self.detail_url,
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        @patch.dict("os.environ", {"PORTFOLIO_SECRET": "test-secret"})
        def test_delete_with_wrong_security_code(self):
            self.client.force_authenticate(user=self.owner)

            response = self.client.delete(
                self.detail_url,
                {"secret": "wrong-secret"},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            self.assertTrue(
                PreviousWork.objects.filter(
                    pk=self.previous_work.id
                ).exists()
            )


class EducationAPITest(APITestCase):
    def setUp(self):
        # Membuat user owner
        self.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="ownerpassword123",
        )

        # Membuat user biasa
        self.visitor = User.objects.create_user(
            username="visitor",
            email="visitor@example.com",
            password="visitorpassword123",
        )

        # Membuat user editor
        self.editor = User.objects.create_user(
            username="editor",
            email="editor@example.com",
            password="editorpassword123",
        )

        # Memasukkan editor ke group Editor
        self.editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(self.editor_group)

        # Endpoint API Education
        self.list_url = reverse("api:education-list")

        # Data Education untuk pengujian
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            year="2025 - Present",
            achievements="Mahasiswa Ilmu Komputer",
        )

        self.detail_url = reverse(
            "api:education-detail",
            args=[self.education.id],
        )

        self.star_url = reverse(
            "api:education-star",
            args=[self.education.id],
        )

        self.payload = {
            "institution": "Institut Teknologi Bandung",
            "degree": "S1 Teknik Informatika",
            "year": "2024 - 2028",
            "achievements": "Mahasiswa berprestasi",
        }

    # 1. Pengunjung dapat melihat daftar dan detail Education
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(
                item["institution"] == "Universitas Indonesia"
                for item in response.data
            )
        )

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["institution"],
            "Universitas Indonesia",
        )

    # 2. Pengujian pencarian Education
    def test_search_and_empty_result(self):
        response = self.client.get(
            self.list_url,
            {"institution": "Universitas"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(
                item["institution"] == "Universitas Indonesia"
                for item in response.data
            )
        )

        response = self.client.get(
            self.list_url,
            {"institution": "Tidak Ditemukan"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # 3. Pengujian Education yang tidak ditemukan
    def test_missing_education(self):
        missing_url = reverse(
            "api:education-detail",
            args=[999999],
        )

        response = self.client.get(missing_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # 4. Guest dan visitor tidak dapat membuat Education
    def test_guest_and_visitor_cannot_write(self):
        # Guest / belum login
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Visitor / user biasa
        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # 5. Owner dapat membuat Education
    def test_owner_can_create_education(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Education.objects.filter(
                institution="Institut Teknologi Bandung"
            ).exists()
        )

    # 6. Pengujian validasi input
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        for changes, field in [
            ({"institution": "   "}, "institution"),
            (
                {"institution": '<img src="x" onerror="alert(1)">'},
                "institution",
            ),
            ({"year": "   "}, "year"),
        ]:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

            self.assertIn(field, response.data)

    # 7. Owner dapat PATCH, PUT, dan DELETE Education
    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # PATCH: mengubah sebagian data
        response = self.client.patch(
            self.detail_url,
            {"institution": "Universitas Gadjah Mada"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.education.refresh_from_db()

        self.assertEqual(
            self.education.institution,
            "Universitas Gadjah Mada",
        )

        # PUT: mengganti seluruh data
        put_payload = {
            "institution": "Universitas Brawijaya",
            "degree": "S1 Sistem Informasi",
            "year": "2025 - 2029",
            "achievements": "Mahasiswa aktif",
        }

        response = self.client.put(
            self.detail_url,
            put_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.education.refresh_from_db()

        self.assertEqual(
            self.education.institution,
            "Universitas Brawijaya",
        )

        # DELETE: menghapus Education
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Education.objects.filter(
                id=self.education.id
            ).exists()
        )

    # 8. Pengujian fitur star Education
    def test_star_toggle(self):
        self.client.force_authenticate(user=self.visitor)

        # Star pertama
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            self.education.starred_by.filter(
                id=self.visitor.id
            ).exists()
        )

        # Star kedua: menghapus star
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            self.education.starred_by.filter(
                id=self.visitor.id
            ).exists()
        )

    # 9. Field hasil perhitungan tidak dapat diubah oleh user
    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.payload,
            "star_count": 999,
            "is_starred": True,
            "starred_by_names": "hacker",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    # 10. Staff / Editor tidak dapat mengelola Education
    def test_staff_and_editor_cannot_manage_education(self):
        self.client.force_authenticate(user=self.editor)

        # Editor tidak boleh membuat Education
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Editor boleh mengubah Education dengan PATCH
        response = self.client.patch(
            self.detail_url,
            {"institution": "Universitas Baru"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
    # 11. Pengujian HTTP method yang tidak diizinkan
    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    # 12. Session write tanpa CSRF token ditolak
    def test_session_write_without_csrf_is_rejected(self):
        csrf_client = APIClient(enforce_csrf_checks=True)

        csrf_client.login(
            username="owner",
            password="ownerpassword123",
        )

        response = csrf_client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # 13. Session write dengan CSRF token berhasil
    def test_session_write_with_csrf_succeeds(self):
        csrf_client = APIClient(enforce_csrf_checks=True)

        csrf_client.login(
            username="owner",
            password="ownerpassword123",
        )

        # Mengambil CSRF cookie
        csrf_client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        csrf_token = csrf_client.cookies["csrftoken"].value

        response = csrf_client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )


class ExperienceAPITest(APITestCase):
    def setUp(self):
        # Membuat user owner
        self.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="ownerpassword123",
        )

        # Membuat user biasa
        self.visitor = User.objects.create_user(
            username="visitor",
            email="visitor@example.com",
            password="visitorpassword123",
        )

        # Membuat user editor
        self.editor = User.objects.create_user(
            username="editor",
            email="editor@example.com",
            password="editorpassword123",
        )

        # Memasukkan editor ke group Editor
        self.editor_group, _ = Group.objects.get_or_create(
            name="Editor"
        )
        self.editor.groups.add(self.editor_group)

        # Endpoint API Experience
        self.list_url = reverse("api:experience-list")

        # Membuat data Experience untuk pengujian
        self.experience = Experience.objects.create(
            title="Software Engineer Intern",
            description="Developing web applications",
            category="internship",
            thumbnail="https://example.com/thumbnail.jpg",
            started_at=timezone.now(),
            ended_at=None,
        )

        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )

        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

        # Payload untuk membuat Experience baru
        self.payload = {
            "title": "Research Assistant",
            "description": "Conducting research in computer science",
            "category": "research",
            "thumbnail": "https://example.com/research.jpg",
            "started_at": "2025-03-01T00:00:00Z",
            "ended_at": "2025-06-01T00:00:00Z",
        }

    # 1. Pengunjung dapat melihat daftar dan detail Experience
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            any(
                item["title"] == "Software Engineer Intern"
                for item in response.data
            )
        )

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Software Engineer Intern",
        )

    # 2. Pengujian pencarian Experience
    def test_search_and_empty_result(self):
        response = self.client.get(
            self.list_url,
            {"title": "Software"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            any(
                item["title"] == "Software Engineer Intern"
                for item in response.data
            )
        )

        response = self.client.get(
            self.list_url,
            {"title": "Tidak Ditemukan"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 0)

    # 3. Pengujian Experience yang tidak ditemukan
    def test_missing_experience(self):
        missing_id = uuid.uuid4()

        missing_url = reverse(
            "api:experience-detail",
            args=[missing_id],
        )

        response = self.client.get(missing_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # 4. Guest dan visitor tidak dapat membuat Experience
    def test_guest_and_visitor_cannot_write(self):
        # Guest / belum login
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Visitor / user biasa
        self.client.force_authenticate(
            user=self.visitor
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # 5. Owner dapat membuat Experience
    def test_owner_can_create_experience(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Experience.objects.filter(
                title="Research Assistant"
            ).exists()
        )

    # 6. Pengujian validasi input
    def test_validation(self):
        self.client.force_authenticate(
            user=self.owner
        )

        for changes, field in [
            ({"title": "   "}, "title"),
            (
                {"title": '<img src="x" onerror="alert(1)">'},
                "title",
            ),
        ]:
            response = self.client.post(
                self.list_url,
                {**self.payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

            self.assertIn(field, response.data)

    # 7. Owner dapat PATCH, PUT, dan DELETE Experience
    def test_patch_put_and_delete(self):
        self.client.force_authenticate(
            user=self.owner
        )

        # PATCH: mengubah sebagian data
        response = self.client.patch(
            self.detail_url,
            {"title": "Backend Developer Intern"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Backend Developer Intern",
        )

        # PUT: mengganti seluruh data
        put_payload = {
            "title": "Full Stack Developer",
            "description": "Building full stack applications",
            "category": "full-time",
            "thumbnail": "https://example.com/fullstack.jpg",
            "started_at": "2025-01-01T00:00:00Z",
            "ended_at": "2025-12-31T00:00:00Z",
        }

        response = self.client.put(
            self.detail_url,
            put_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Full Stack Developer",
        )

        # DELETE: menghapus Experience
        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Experience.objects.filter(
                id=self.experience.id
            ).exists()
        )

    # 8. Pengujian fitur star Experience
    def test_star_toggle(self):
        self.client.force_authenticate(
            user=self.visitor
        )

        # Star pertama
        response = self.client.post(
            self.star_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            self.experience.starred_by.filter(
                id=self.visitor.id
            ).exists()
        )

        self.assertEqual(
            response.data["star_count"],
            1,
        )

        # Star kedua: menghapus star
        response = self.client.post(
            self.star_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            self.experience.starred_by.filter(
                id=self.visitor.id
            ).exists()
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )

    # 9. Computed fields tidak dapat diubah oleh user
    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(
            user=self.owner
        )

        payload = {
            **self.payload,
            "is_ongoing": True,
            "star_count": 999,
            "is_starred": True,
            "starred_by_names": "hacker",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertFalse(
            response.data["is_ongoing"]
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )

        self.assertFalse(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["starred_by_names"],
            "",
        )

    # 10. Editor tidak boleh membuat atau menghapus Experience,
    # tetapi boleh melakukan PATCH dan PUT
    def test_staff_and_editor_permissions(self):
        self.client.force_authenticate(
            user=self.editor
        )

        # Editor tidak boleh membuat Experience
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Editor boleh melakukan PATCH
        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Editor boleh melakukan PUT
        put_payload = {
            "title": "Updated Experience",
            "description": "Updated description",
            "category": "research",
            "thumbnail": "",
            "started_at": "2025-01-01T00:00:00Z",
            "ended_at": "2025-12-31T00:00:00Z",
        }

        response = self.client.put(
            self.detail_url,
            put_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Editor tidak boleh menghapus Experience
        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # 11. Pengujian HTTP method yang tidak diizinkan
    def test_wrong_method(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.delete(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # 12. Session write tanpa CSRF token ditolak
    def test_session_write_without_csrf_is_rejected(self):
        csrf_client = APIClient(
            enforce_csrf_checks=True
        )

        csrf_client.login(
            username="owner",
            password="ownerpassword123",
        )

        response = csrf_client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # 13. Session write dengan CSRF token berhasil
    def test_session_write_with_csrf_succeeds(self):
        csrf_client = APIClient(
            enforce_csrf_checks=True
        )

        csrf_client.login(
            username="owner",
            password="ownerpassword123",
        )

        # Mengambil CSRF cookie
        csrf_client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        csrf_token = csrf_client.cookies["csrftoken"].value

        response = csrf_client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
