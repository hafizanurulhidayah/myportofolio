from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.core import serializers
from django.contrib.auth import login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied    
from django.views.decorators.http import require_POST 

 

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

def show_profile(request, username):
    profile_user = get_object_or_404(User,username=username)

    starred_experiences = profile_user.starred_experience.all()
    starred_educations = profile_user.starred_education.all()
    starred_previousworks = profile_user.starred_previouswork.all()

    if profile_user.is_superuser:
        role = "Owner"
    elif profile_user.groups.filter(name="Editor").exists():
        role = "Editor"
    else:
        role = "User"

    total_starred = (
        starred_experiences.count()
        + starred_educations.count()
        + starred_previousworks.count()
    )

    return render(
        request,
        "profile.html",
        {
            "profile_user": profile_user,
            "role": role,
            "starred_experiences": starred_experiences,
            "starred_educations": starred_educations,
            "starred_previousworks": starred_previousworks,
            "total_starred": total_starred,
        }
    )

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")


@login_required(login_url="/login/")
def toggle_star_previouswork(request, previouswork_id):
    previouswork = get_object_or_404(PreviousWork, pk=previouswork_id)

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in previouswork.starred_by.all():
            previouswork.starred_by.remove(request.user)
        else:
            previouswork.starred_by.add(request.user)

    return redirect("main:show_previous_work")

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
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "title_query": title_query,
        "form": ExperienceForm(),
    }

    return render(request, "experience.html", context)

def show_previous_work(request):
    search_query = request.GET.get("search", "").strip()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "search_query": search_query,
         "form": PreviousWorkForm(),
    }

    return render(
        request,
        "PreviousWork.html",
        context
    )
def show_education(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Hafiza Nurul Hidayah",
        "title_query": title_query,
        "form": EducationForm(),
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
    educations = Education.objects.prefetch_related("starred_by").all()

    if title_query:
        educations = educations.filter(
            institution__icontains=title_query
        )

    data = []

    for education in educations:
        starred_users = education.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [u.username for u in starred_users]
        )

        data.append({
            "pk": str(education.id),
            "fields": {
                "institution": education.institution,
                "degree": education.degree,
                "year": education.year,
                "achievements": education.achievements,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(
            title__icontains=title_query
        )

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()

        is_starred = (
            starred_users.filter(pk=request.user.pk).exists()
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [u.username for u in starred_users]
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.get_category_display(),
                "started_at": (
                    experience.started_at.isoformat()
                    if experience.started_at
                    else None
                ),
                "ended_at": (
                    experience.ended_at.isoformat()
                    if experience.ended_at
                    else None
                ),
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def get_previous_work_json(request):
    title_query = request.GET.get("title", "").strip()
    previouswork = PreviousWork.objects.prefetch_related("starred_by").all()

    if title_query:
        previouswork = previouswork.filter(
            title__icontains=title_query
        )

    data = []

    for work in previouswork:
        starred_users = work.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [u.username for u in starred_users]
        )

        data.append({
            "pk": str(work.id),
            "fields": {
                "title": work.title,
                "role": work.role,
                "description": work.description,
                "date": work.date,
                "category": work.category,
                "link": work.link,
                "photo": work.photo.url if work.photo else None,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

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
@login_required(login_url="/login/") 
def update_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        id=experience_id
    )

    if not request.user.has_perm("main.change_experience"):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_education(request, education_id):
    education = get_object_or_404(
        Education,
        id=education_id
    )

    if not request.user.has_perm("main.change_education"):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_previous_work(request, previous_work_id):
    previous_work = get_object_or_404(
        PreviousWork,
        pk=previous_work_id
    )

    if not request.user.has_perm("main.change_previouswork"):
        raise PermissionDenied

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

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)