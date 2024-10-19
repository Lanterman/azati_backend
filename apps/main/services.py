from . import db_queries
from apps.user.models import User


DICT_LEVEL = {"BEGINNER": 1, "INTERMEDIATE": 2, "ADVANCED": 3}


def get_sorted_list(dict_assessment: dict) -> list:
    """Get a sorted list from a dictionary. Sort by dictionary values."""

    sorted_list = sorted(dict_assessment.items(), key=lambda x: x[1], reverse=True)
    return list(item[0] for item in sorted_list)


def get_list_of_sorted_vacancies(user: User) -> list:
    """Get a list sorted by the jobs most relevant to the user"""

    relevant_skills = db_queries.get_relevant_vacancies_skills([skill.skill_name for skill in user.skills.all()])
    vacancies = db_queries.get_vacancies_by_relevant_skill([skill.vacancy_id_id for skill in relevant_skills])

    dict_assessment = {vacancy: 0 for vacancy in vacancies}

    for skill in relevant_skills:
        dict_assessment[skill.vacancy_id] += DICT_LEVEL[skill.min_level] + skill.min_years_of_experience
    
    return get_sorted_list(dict_assessment)


def get_list_of_sorted_candidates(vacancy_id: int) -> list:
    """Get a list of candidates sorted by the users most suitable for the job"""

    vacancy_skills = db_queries.get_vacancy_skills_by_vacancy_id(vacancy_id)
    relevant_skills = db_queries.get_relevant_candidates_skills([skill.skill_name for skill in vacancy_skills])
    users = db_queries.get_candicates_by_relevant_skill([skill.user_id_id for skill in relevant_skills])

    dict_assessment = {user: 0 for user in users}

    for skill in relevant_skills:
        dict_assessment[skill.user_id] += DICT_LEVEL[skill.level] + skill.years_of_experience

    return get_sorted_list(dict_assessment)
