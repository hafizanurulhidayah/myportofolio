from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Hafiza Nurul Hidayah",
        "npm": "2506624101",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
           "Im currently pursuing a Computer Science degree at Universitas Indonesia "
           "Actively exploring software engineering and collaborative tech initiatives. "
           "Im always open to connecting and sharing insights on technology."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Hafiza Nurul Hidayah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

