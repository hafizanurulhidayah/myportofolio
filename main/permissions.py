from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ["POST", "DELETE"]:
            return (
                request.user.is_authenticated
                and request.user.is_superuser
            )

        if request.method in ["PUT", "PATCH"]:
            return (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.has_perm("main.change_previouswork")
                )
            )

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == "DELETE":
            return (
                request.user.is_authenticated
                and request.user.is_superuser
            )

        if request.method in ["PUT", "PATCH"]:
            return (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.has_perm("main.change_previouswork")
                )
            )

        return False

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )