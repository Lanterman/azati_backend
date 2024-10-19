from . import db_queries
from apps.user.models import User


DICT_LEVEL = {"BEGINNER": 1, "INTERMEDIATE": 2, "ADVANCED": 3}


def get_sorted_list_quick_sort(list_assessment: dict) -> list:
    """Get a sorted list by quick sort algorithm"""

    if len(list_assessment) <= 1:
        return list_assessment
    
    pivot = list_assessment[len(list_assessment) // 2]

    left = [item for item in list_assessment if item[1] < pivot[1]]
    middle = [item for item in list_assessment if item[1] == pivot[1]]
    right = [item for item in list_assessment if item[1] > pivot[1]]

    return get_sorted_list_quick_sort(right) + middle + get_sorted_list_quick_sort(left)


def get_sorted_list(dict_assessment: dict) -> list:
    """Get a sorted list from a dictionary. Sort by dictionary values."""

    return sorted(dict_assessment.items(), key=lambda x: x[1], reverse=True)


def get_list_of_sorted_vacancies(user: User) -> list:
    """Get a list sorted by the jobs most relevant to the user"""

    relevant_skills = db_queries.get_relevant_vacancies_skills([skill.skill_name for skill in user.skills.all()])
    vacancies = db_queries.get_vacancies_by_relevant_skill([skill.vacancy_id_id for skill in relevant_skills])

    dict_assessment = {vacancy: 0 for vacancy in vacancies}

    for skill in relevant_skills:
        dict_assessment[skill.vacancy_id] += DICT_LEVEL[skill.min_level] + skill.min_years_of_experience
    
    ## sort by lambda function
    # sorted_list = get_sorted_list(dict_assessment)
    
    ## quick sort algorithm
    sorted_list = get_sorted_list_quick_sort([(key, value) for key, value in dict_assessment.items()])

    return list(item[0] for item in sorted_list)


def get_list_of_sorted_candidates(vacancy_id: int) -> list:
    """Get a list of candidates sorted by the users most suitable for the job"""

    vacancy_skills = db_queries.get_vacancy_skills_by_vacancy_id(vacancy_id)
    relevant_skills = db_queries.get_relevant_candidates_skills([skill.skill_name for skill in vacancy_skills])
    users = db_queries.get_candicates_by_relevant_skill([skill.user_id_id for skill in relevant_skills])

    dict_assessment = {user: 0 for user in users}

    for skill in relevant_skills:
        dict_assessment[skill.user_id] += DICT_LEVEL[skill.level] + skill.years_of_experience

    ## sort by lambda function
    # sorted_list = get_sorted_list(dict_assessment)
    
    ## quick sort algorithm
    sorted_list = get_sorted_list_quick_sort([(key, value) for key, value in dict_assessment.items()])
    
    return list(item[0] for item in sorted_list)
