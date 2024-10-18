from django.contrib import admin

from . import models


class RecruiterSkillInlince(admin.TabularInline):
    """Options for inline editing of RecruiterSkill `model` instances."""

    model = models.RecruiterSkill
    extra = 4
    max_num = 4


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Vacancy admin"""

    list_display = ("id", "owner_id")
    list_display_links = ("id", "owner_id")
    fields = ("owner_id",)
    list_max_show_all = 250
    list_per_page = 150
    inlines = [RecruiterSkillInlince]


@admin.register(models.CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    """CandidateSkill admin"""

    list_display = ("id", "skill_name", "level", "years_of_experience", "last_used_year", "user_id")
    list_display_links = ("id", "skill_name", "level", "years_of_experience", "last_used_year", "user_id")
    fields = ("skill_name", "level", "years_of_experience", "last_used_year", "user_id")
    search_fields = ("skill_name ", )
    list_filter = ("level", "last_used_year")
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True


@admin.register(models.RecruiterSkill)
class RecruiterSkillAdmin(admin.ModelAdmin):
    """RecruiterSkill admin"""

    list_display = ("id", "skill_name", "min_level", "min_years_of_experience", "vacancy_id")
    list_display_links = ("id", "skill_name", "min_level", "min_years_of_experience", "vacancy_id")
    fields = ("skill_name", "min_level", "min_years_of_experience", "vacancy_id")
    search_fields = ("skill_name ", )
    list_filter = ("min_level", "min_years_of_experience")
    list_max_show_all = 250
    list_per_page = 150
    list_select_related = True
