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
from main.models import PreviousWork
from main.forms import PreviousWorkForm



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

# ini blm gw ubah ya 

def show_previous_work(request):
    previous_work_list = PreviousWork.objects.all()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "previous_work_list": previous_work_list,
    }

    return render(
        request,
        "PreviousWork.html",
        context
    )


def show_educations(request):
    education_list = Education.objects.all()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "education_list": education_list,
        "title_query": request.GET.get("title", "").strip(),
    }

    return render(request, "education.html", context)


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

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
          secret = request.POST.get("secret")
          env_secret = os.getenv("PORTFOLIO_SECRET")
  
          print("SECRET DARI FORM:", repr(secret))
          print("SECRET DARI ENV :", repr(env_secret))
  
          if secret != env_secret:
              messages.error(request, "Security Code salah!")
              return redirect("main:show_education")
  
          education.delete()
          messages.success(request, "Education berhasil dihapus!")
          return redirect("main:show_education")



def delete_previous_work(request, previous_work_id):
    previous_work = get_object_or_404(
        PreviousWork,
        pk=previous_work_id
    )

    if request.method == "POST":
        secret = request.POST.get("secret")
        env_secret = os.getenv("PORTFOLIO_SECRET")

        if secret != env_secret:
            messages.error(
                request,
                "Security Code salah!"
            )
            return redirect("main:show_previous_work")

        previous_work.delete()

        messages.success(
            request,
            "Previous Work berhasil dihapus!"
        )

    return redirect("main:show_previous_work")


 

def get_education_json(request):
    title_query = request.GET.get("title", "").strip()
    educations = Education.objects.all()

    if title_query:
        educations = Education.objects.filter(
            institution__icontains=title_query
        )

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = Experience.objects.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def get_previous_work_json(request):
    title_query = request.GET.get("title", "").strip()
    previouswork = PreviousWork.objects.all()

    if title_query:
        previouswork = previouswork.filter(title__icontains=title_query)

    previouswork_json = serializers.serialize("json", previouswork)
    return HttpResponse(previouswork_json, content_type="application/json")

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        secret = form.cleaned_data["secret"]

        if secret != os.getenv("PORTFOLIO_SECRET"):
            messages.error(request, "Secret code salah!")
            return render(request, "education_form.html", {
                "name": "Hafiza",
                "form": form,
            })

        form.save()
        messages.success(request, "Education baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Hafiza",
        "form": form,  # ← INI
    }

    return render(request, "education_form.html", context)

def create_previous_work(request):
    form = PreviousWorkForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":
        if form.is_valid():

            secret = form.cleaned_data["secret"]
            env_secret = os.getenv("PORTFOLIO_SECRET")

            if secret != env_secret:
                messages.error(
                    request,
                    "Security Code salah!"
                )
                return render(
                    request,
                    "PreviousWork_form.html",
                    {
                        "name": "Hafiza Nurul Hidayah",
                        "form": form,
                    }
                )

            form.save()

            messages.success(
                request,
                "Previous Work berhasil ditambahkan!"
            )

            return redirect("main:show_previous_work")

    context = {
        "name": "Hafiza Nurul Hidayah",
        "form": form,
    }

    return render(
        request,
        "PreviousWork_form.html",
        context
    )


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
