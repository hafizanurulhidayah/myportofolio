
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import PreviousWork


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


    def test_patch_put_and_delete(self):
        self.client.force_authenticate(
            user=self.owner,
        )

        # PATCH hanya mengubah judul
        response = self.client.patch(
            self.detail_url,
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.previous_work.refresh_from_db()

        self.assertEqual(
            self.previous_work.title,
            "Changed",
        )

        self.assertEqual(
        self.previous_work.description,
        "My website",
    )
        # PUT dengan data tidak lengkap
        response = self.client.put(
            self.detail_url,
            {"title": "Incomplete"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        # PUT dengan data lengkap
        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # DELETE
        response = self.client.delete(
            self.detail_url,
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
