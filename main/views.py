from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied       

import os
import datetime

from dotenv import load_dotenv

load_dotenv()



from main.forms import EducationForm
from main.forms import ExperienceForm
from main.models import Experience
from main.models import Education
from main.models import PreviousWork
from main.forms import PreviousWorkForm

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Hafiza Nurul Hidayah",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Hafiza Nurul Hidayah",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
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

def show_previous_work(request):
    search_query = request.GET.get("search", "").strip()

    previous_work_list = PreviousWork.objects.all()

    if search_query:
        previous_work_list = previous_work_list.filter(
            Q(title__icontains=search_query)
            | Q(role__icontains=search_query)
            | Q(category__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    context = {
        "name": "Hafiza Nurul Hidayah",
        "previous_work_list": previous_work_list,
        "search_query": search_query,
    }

    return render(
        request,
        "PreviousWork.html",
        context
    )


def show_education(request):
    title_query = request.GET.get("title", "").strip()

    education_list = Education.objects.all()

    if title_query:
        education_list = education_list.filter(
            institution__icontains=title_query
        )

    for education in education_list:
        education.achievements_list = education.achievements.splitlines()


    context = {
        "name": "Hafiza Nurul Hidayah",
        "education_list": education_list,
        "title_query": title_query,
    }

    return render(request, "education.html", context)

@login_required(login_url="/login/") 
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
            raise PermissionDenied
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

@login_required(login_url="/login/") 
def delete_education(request, education_id):
    if not request.user.is_superuser:
            raise PermissionDenied
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


@login_required(login_url="/login/") 
def delete_previous_work(request, previous_work_id):
    if not request.user.is_superuser:
            raise PermissionDenied
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

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")

def get_previous_work_json(request):
    title_query = request.GET.get("title", "").strip()
    previouswork = PreviousWork.objects.all()

    if title_query:
        previouswork = previouswork.filter(title__icontains=title_query)

    previouswork_json = serializers.serialize("json", previouswork)
    return HttpResponse(previouswork_json, content_type="application/json")

@login_required(login_url="/login/") 
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        secret = form.cleaned_data["secret"]

        if secret != os.getenv("PORTFOLIO_SECRET"):
            messages.error(request, "Secret code salah!")
            return render(
                request,
                "education_form.html",
                {
                    "name": "Hafiza",
                    "form": form,
                    "page_title": "Add New Education",
                    "button_text": "Tambah Education",
                }
            )

        form.save()
        messages.success(
            request,
            "Education baru berhasil ditambahkan!"
        )
        return redirect("main:show_education")

    return render(
        request,
        "education_form.html",
        {
            "name": "Hafiza",
            "form": form,
            "page_title": "Add New Education",
            "button_text": "Tambah Education",
        }
    )

@login_required(login_url="/login/") 
def create_previous_work(request):
    if not request.user.is_superuser:
            raise PermissionDenied
     
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
                        "page_title": "Add Previous Work",
                        "button_text": "Simpan",
                    }
                )

            form.save()

            messages.success(
                request,
                "Previous Work berhasil ditambahkan!"
            )

            return redirect("main:show_previous_work")

    return render(
        request,
        "PreviousWork_form.html",
        {
            "name": "Hafiza Nurul Hidayah",
            "form": form,
            "page_title": "Add Previous Work",
            "button_text": "Simpan",
        }
    )


@login_required(login_url="/login/") 
def create_experience(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    form = ExperienceForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        secret = form.cleaned_data["secret"]

        if secret != os.getenv("PORTFOLIO_SECRET"):
            messages.error(request, "Secret code salah!")
            return render(
                request,
                "experience_form.html",
                {
                    "name": "Hafiza",
                    "form": form,
                    "page_title": "Add New Experience",
                    "button_text": "Tambah Experience",
                }
            )

        form.save()
        messages.success(
            request,
            "Experience baru berhasil ditambahkan!"
        )
        return redirect("main:show_experience")

    return render(
        request,
        "experience_form.html",
        {
            "name": "Hafiza",
            "form": form,
            "page_title": "Add New Experience",
            "button_text": "Tambah Experience",
        }
    )

# update 
def update_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        id=experience_id
    )

    if request.method == "POST":
        form = ExperienceForm(
            request.POST,
            request.FILES,
            instance=experience
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Experience berhasil diperbarui!"
            )
            return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)

    return render(
        request,
        "experience_form.html",
        {
            "name": "Hafiza",
            "form": form,
            "page_title": "Edit Experience",
            "button_text": "Simpan Perubahan",
            "experience": experience,
        }
    )

def update_education(request, education_id):
    education = get_object_or_404(
        Education,
        id=education_id
    )

    if request.method == "POST":
        form = EducationForm(
            request.POST,
            instance=education
        )

        if form.is_valid():
            secret = form.cleaned_data["secret"]

            if secret != os.getenv("PORTFOLIO_SECRET"):
                messages.error(request, "Secret code salah!")

                return render(
                    request,
                    "education_form.html",
                    {
                        "name": "Hafiza",
                        "form": form,
                        "page_title": "Edit Education",
                        "button_text": "Simpan Perubahan",
                        "education": education,
                    }
                )

            form.save()

            messages.success(
                request,
                "Education berhasil diperbarui!"
            )

            return redirect("main:show_education")

    else:
        form = EducationForm(
            instance=education
        )

    return render(
        request,
        "education_form.html",
        {
            "name": "Hafiza",
            "form": form,
            "page_title": "Edit Education",
            "button_text": "Simpan Perubahan",
            "education": education,
        }
    )

def update_previous_work(request, previous_work_id):
    previous_work = get_object_or_404(
        PreviousWork,
        pk=previous_work_id
    )

    if request.method == "POST":
        form = PreviousWorkForm(
            request.POST,
            request.FILES,
            instance=previous_work
        )

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
                        "page_title": "Edit Previous Work",
                        "button_text": "Simpan Perubahan",
                        "previous_work": previous_work,
                    }
                )

            form.save()

            messages.success(
                request,
                "Previous Work berhasil diperbarui!"
            )

            return redirect("main:show_previous_work")

    else:
        form = PreviousWorkForm(
            instance=previous_work
        )

    return render(
        request,
        "PreviousWork_form.html",
        {
            "name": "Hafiza Nurul Hidayah",
            "form": form,
            "page_title": "Edit Previous Work",
            "button_text": "Simpan Perubahan",
            "previous_work": previous_work,
        }
    )