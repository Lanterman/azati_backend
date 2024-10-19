from rest_framework.test import APITestCase

from apps.main import models


class TestVacancyModel(APITestCase):
    """Testing Vacancy model"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.vacancy_1 = models.Vacancy.objects.get(id=1)
        cls.vacancy_2 = models.Vacancy.objects.get(id=2)
            
    def test__str__method(self):
        """Testing __str__ method"""

        resposne = self.vacancy_1.__str__()
        assert resposne == "Vacancy 1", resposne

        resposne = self.vacancy_2.__str__()
        assert resposne == "Vacancy 2", resposne
    
    def test_get_absolute_url_method(self):
        """Testing get_absolute_url method"""

        response = self.vacancy_1.get_absolute_url()
        assert response == "/api/v1/vacancies/1/", response

        response = self.vacancy_2.get_absolute_url()
        assert response == "/api/v1/vacancies/2/", response
