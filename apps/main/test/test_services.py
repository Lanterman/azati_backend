import pytest

from rest_framework.test import APITestCase

from apps.main import services
from apps.user.models import User


@pytest.mark.parametrize("test_input, output", [
    ({"user_1": 1, "user_2": 2, "user_3": 3 , "user_4": 4}, ["user_4", "user_3", "user_2", "user_1"]), 
    ({"user_1": 3, "user_2": 1, "user_3": 10, "user_4": 5}, ["user_3", "user_4", "user_1", "user_2"]), 
    ({"user_1": 99, "user_2": 80, "user_3": 70, "user_4": 5}, ["user_1", "user_2", "user_3", "user_4"])
])
def test_get_sorted_list(test_input: int | None, output: int):
    """Testing the get_sorted_list function"""

    response = services.get_sorted_list(test_input)
    assert output == response, response


class TestGetListOfSortedVacanciesFunction(APITestCase):
    """Testing the get_list_of_sorted_vacancies function"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=2)

    def test_get_list_of_sorted_vacancies(self):
        # user_1
        response = services.get_list_of_sorted_vacancies(self.user_1)
        list_vacancy_id = [vacancy.id for vacancy in response]
        assert 7 == len(response), len(response)
        assert [3, 5, 2, 6, 9, 7, 1] == list_vacancy_id, list_vacancy_id

        # user_2
        response = services.get_list_of_sorted_vacancies(self.user_2)
        list_vacancy_id = [vacancy.id for vacancy in response]
        assert 9 == len(response), len(response)
        assert [2, 5, 6, 9, 3, 1, 8, 7, 4] == list_vacancy_id, list_vacancy_id


class TestGetListOfSortedCandidatesFunction(APITestCase):
    """Testing the get_list_of_sorted_candidates function"""

    fixtures = ["./config/test/test_data.json"]

    def test_get_list_of_sorted_vacancies(self):
        # vacancy_1
        response = services.get_list_of_sorted_candidates(1)
        list_candidate_id = [candidate.id for candidate in response]
        assert 6 == len(response), len(response)
        assert [6, 7, 2, 1, 5, 4] == list_candidate_id, list_candidate_id

        # vacancy_2
        response = services.get_list_of_sorted_candidates(2)
        list_candidate_id = [candidate.id for candidate in response]
        assert 6 == len(response), len(response)
        assert [6, 7, 2, 4, 1, 5] == list_candidate_id, list_candidate_id
