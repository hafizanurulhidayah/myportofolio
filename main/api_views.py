import os
import secrets

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import (
    PreviousWork,
    Experience,
    Education,
)
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializer import ProjectSerializer, ExperienceSerializer, EducationSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        previous_works = (
            PreviousWork.objects
            .prefetch_related("starred_by")
            .order_by("title", "id")
        )

        title = request.query_params.get("title", "").strip()

        if title:
            previous_works = previous_works.filter(
                title__icontains=title
            )

        serializer = ProjectSerializer(
            previous_works,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    serializer = ProjectSerializer(
        data=request.data,
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):
    previous_work = get_object_or_404(
        PreviousWork.objects.prefetch_related("starred_by"),
        pk=project_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(
            previous_work,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method == "DELETE":
        secret = request.data.get("secret")
        env_secret = os.getenv("PORTFOLIO_SECRET")

        if not env_secret:
            return Response(
                {"detail": "Security Code belum dikonfigurasi di server."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not secret or not secrets.compare_digest(
            str(secret),
            env_secret
        ):
            raise PermissionDenied("Security Code salah!")

        previous_work.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        previous_work,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    previous_work = get_object_or_404(
        PreviousWork.objects.prefetch_related("starred_by"),
        pk=project_id,
    )

    if previous_work.starred_by.filter(
        pk=request.user.pk
    ).exists():
        previous_work.starred_by.remove(request.user)
    else:
        previous_work.starred_by.add(request.user)

    serializer = ProjectSerializer(
        previous_work,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = (
            Experience.objects
            .prefetch_related("starred_by")
            .order_by("-started_at", "title")
        )

        title = request.query_params.get("title", "").strip()

        if title:
            experiences = experiences.filter(
                title__icontains=title
            )

        serializer = ExperienceSerializer(
            experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        educations = (
            Education.objects
            .prefetch_related("starred_by")
            .order_by("institution", "id")
        )

        institution = request.query_params.get(
            "institution", ""
        ).strip()

        if institution:
            educations = educations.filter(
                institution__icontains=institution
            )

        serializer = EducationSerializer(
            educations,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = EducationSerializer(
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=experience_id,
    )

    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    serializer = ExperienceSerializer(
        experience,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"),
        pk=education_id,
    )

    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

    serializer = EducationSerializer(
        education,
        context={"request": request},
    )

    return Response(serializer.data)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=experience_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    elif request.method == "DELETE":
        expected_secret = os.environ.get("PORTFOLIO_SECRET")
        provided_secret = request.data.get("secret", "")

        if not expected_secret:
            raise PermissionDenied("Security Code is not configured.")

        if not secrets.compare_digest(provided_secret, expected_secret):
            return Response(
                {"detail": "Security Code salah."},
                status=status.HTTP_400_BAD_REQUEST
            )

        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"),
        pk=education_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(
            education,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method == "DELETE":
        secret = request.data.get("secret")
        env_secret = os.getenv("PORTFOLIO_SECRET")

        if not env_secret or not secret or not secrets.compare_digest(
            secret,
            env_secret
        ):
            return Response(
                {"detail": "Security Code salah!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)




