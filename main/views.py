from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
import os

from dotenv import load_dotenv

load_dotenv()



from main.forms import EducationForm
from main.forms import ExperienceForm
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
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "experience_list": experiences,
        "title_query": title_query,
    }

    return render(request, "experience.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        secret = request.POST.get("secret")
        env_secret = os.getenv("PORTFOLIO_SECRET")

        print("SECRET DARI FORM:", repr(secret))
        print("SECRET DARI ENV :", repr(env_secret))

        if secret != env_secret:
            messages.error(request, "Security Code salah!")
            return redirect("main:show_experience")

        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_education(request):
    education_list = Education.objects.all()

    for education in education_list:
        education.achievement_list = education.achievements.splitlines()

    context = {
        "education_list": education_list,
    }

    return render(request, "education.html", context)


def get_education_json(request):
    title_query = request.GET.get("title", "").strip()
    educations = Education.objects.all()

    if title_query:
       educations = Education.objects.filter(title__icontains=title_query)

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = Experience.objects.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Hafiza",
        "form": form,
    }
    return render(request, "education_form.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        secret = form.cleaned_data["secret"]

        if secret != os.getenv("PORTFOLIO_SECRET"):
            messages.error(request, "Secret code salah!")
            return render(request, "experience_form.html", {
                "name": "Hafiza",
                "form": form,
            })

        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Hafiza",
        "form": form,
    }
    return render(request, "experience_form.html", context)
