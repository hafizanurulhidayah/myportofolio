from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    Select,
    DateTimeInput,
    PasswordInput,
    CharField,
)


from main.models import Education, Experience


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "year",
            "achievements",
        ]

        labels = {
            "institution": "Institusi Pendidikan",
            "degree": "Gelar / Program Studi",
            "year": "Tahun",
            "achievements": "Pencapaian",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 100,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "Ilmu Komputer",
                    "maxlength": 100,
                }
            ),
            "year": TextInput(
                attrs={
                    "placeholder": "2025 - Sekarang",
                    "maxlength": 20,
                }
            ),
            "achievements": Textarea(
                attrs={
                    "placeholder": "Tuliskan pencapaian selama pendidikan",
                    "rows": 3,
                }
            ),
        }


class ExperienceForm(ModelForm):
    secret = CharField(
        label="Secret Code",
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan secret code",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "thumbnail": "Thumbnail Photo (URL)" ,
            "started_at": "Pengalaman dimulai pada (dd/mm/yy)",
            "ended_at": "Pengalaman selesai pada (dd//mm/yy)",
        }

    widgets = {
        "title": TextInput(
            attrs={
                "placeholder": "Software Engineer Intern",
                "maxlength": 255,
                "class": "form-control",
            }
        ),
        "description": Textarea(
            attrs={
                "placeholder": "Ceritakan pengalaman atau tanggung jawabmu...",
                "rows": 4,
                "class": "form-control",
            }
        ),
        "category": Select(
            attrs={
                "class": "form-control",
            }
        ),
        "thumbnail": TextInput(
            attrs={
                "placeholder": "https://example.com/image.jpg",
                "class": "form-control",
            }
        ),
        "started_at": DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        ),
        "ended_at": DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        ),
    }