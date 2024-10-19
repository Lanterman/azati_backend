from . import models
from apps.user.models import RoleChoice, User


def get_vacancies() -> list:
    """Get vacancies"""

    return models.Vacancy.objects.all().prefetch_related("min_skills")


def get_candidates() -> list:
    """Get candidates"""

    return User.objects.filter(role=RoleChoice.CANDIDATE).prefetch_related("skills")


# for the get_list_of_sorted_vacancies function
def get_relevant_vacancies_skills(skill_names: list) -> list:
    """Get vacancies skills for relevant candidate"""

    return models.RecruiterSkill.objects.filter(skill_name__in=skill_names).select_related("vacancy_id")


def get_vacancies_by_relevant_skill(relevant_skills: list) -> list:
    """Get a list of vacancies for the relevant skills of the candidate"""

    return models.Vacancy.objects.filter(id__in=relevant_skills).prefetch_related("min_skills")


# for the get_list_of_sorted_candidates function
def get_vacancy_skills_by_vacancy_id(vacancy_id: int) -> models.Vacancy:
    """Get vacancy skills by vacancy id"""

    return models.RecruiterSkill.objects.filter(vacancy_id=vacancy_id)


def get_relevant_candidates_skills(skill_names: list) -> list:
    """Get candidates skills for relevant vacancy"""

    return models.CandidateSkill.objects.filter(skill_name__in=skill_names).select_related("user_id")


def get_candicates_by_relevant_skill(relevant_skills: list) -> list:
    """Get a list of candidates for the relevant skills of the vacancy"""

    return User.objects.filter(id__in=relevant_skills).prefetch_related("skills")
