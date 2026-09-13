from django.contrib import admin
from .models import Experience, ExperiencePhoto

# Register your models here.
class ExperiencePhotoInline(admin.TabularInline):
    model = ExperiencePhoto
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [ExperiencePhotoInline]