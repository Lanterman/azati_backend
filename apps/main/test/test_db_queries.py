from rest_framework.test import APITestCase

from apps.main import db_queries, models


class TestGetVacanciesFunction(APITestCase):
    """Testing get_vacancies function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_vacancies(self):
        response = db_queries.get_vacancies()
        assert 9 == len(response), len(response)
        assert 1 == response[0].id, response[0]


class TestGetCandidatesFunction(APITestCase):
    """Testing get_candidates function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_candidates(self):
        response = db_queries.get_candidates()
        assert 5 == len(response), len(response)
        assert "lanterman" == response[0].username, response[0]


class TestGetRelevantVacanciesSkillsFunction(APITestCase):
    """Testing get_relevant_vacancies_skills function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_relevant_vacancies_skills(self):
        response = db_queries.get_relevant_vacancies_skills(["Python", "Java"])
        assert 11 == len(response), len(response)
        assert "Python - 3 minimal years of experience" == response[0].__str__(), response[0]


class TestGetVacanciesByRelevantSkillFunction(APITestCase):
    """Testing get_vacancies_by_relevant_skill function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_vacancies_by_relevant_skill(self):
        response = db_queries.get_vacancies_by_relevant_skill([1, 2, 1])
        assert 2 == len(response), len(response)
        assert "Vacancy 1" == response[0].__str__(), response[0]


class TestGetVacancySkillsByVacantyIdFunction(APITestCase):
    """Testing get_vacancy_skills_by_vacancy_id function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_vacancy_skills_by_vacancy_id(self):
        response = db_queries.get_vacancy_skills_by_vacancy_id(1)
        assert 2 == len(response), len(response)
        assert "Python - 3 minimal years of experience" == response[0].__str__(), response[0]


class TestGetRelevantCandidatesSkillsFunction(APITestCase):
    """Testing get_relevant_candidates_skills function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_relevant_candidates_skills(self):
        response = db_queries.get_relevant_candidates_skills(["Python", "Java", "Redis", "string"])
        assert 9 == len(response), len(response)
        assert "Java - 1 years of experience" == response[0].__str__(), response[0]


class TestGetCandidatesByRelevantSkillFunction(APITestCase):
    """Testing get_candicates_by_relevant_skill function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_candicates_by_relevant_skill(self):
        response = db_queries.get_candicates_by_relevant_skill([1, 2, 3, 2])
        assert 3 == len(response), len(response)
        assert "lanterman" == response[0].username, response[0]
