from django.shortcuts import render

from main.models import Experience
from main.models import Education


def show_main(request):
    experience_list = Experience.objects.all()
    education_list = Education.objects.all()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "npm": "2506624101",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Im currently pursuing a Computer Science degree at Universitas Indonesia "
            "Actively exploring software engineering and collaborative tech initiatives. "
            "Im always open to connecting and sharing insights on technology."
        ),
        "experience_list": experience_list,
        "education_list": education_list,
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Hafiza Nurul Hidayah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_education(request):
    education_list = Education.objects.all()

    for education in education_list:
        education.achievement_list = education.achievements.splitlines()

    context = {
        "education_list": education_list,
    }

    return render(request, "education.html", context)