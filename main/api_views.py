
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

from main.models import PreviousWork
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializer import ProjectSerializer


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
