from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from apps.main import models
from apps.user import models as user_models, services as user_services
from config import settings


class TestIsRecruiterPermission(APITestCase):
    """Testing IsRecruiter class methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = user_models.User.objects.get(id=1)
        cls.user_2 = user_models.User.objects.get(id=3)
        cls.token_1 = user_services.create_jwttoken(cls.user_1.id)
        cls.token_2 = user_services.create_jwttoken(cls.user_2.id)

        cls.request = APIRequestFactory()
        cls.client = APIClient()
        cls.url = reverse('create_vacancy')
        
        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]

    def test_has_object_permission(self):
        """Testing has_object_permission method"""

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        with self.assertLogs(level="WARNING"):
            response_get = self.client.get(path=self.url)
            response_patch = self.client.patch(path=self.url, data={"first_name": "string"})
        assert response_get.status_code == 403, response_get.status_code
        assert response_patch.status_code == 403, response_patch.status_code

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_2.access_token}')
        response_get = self.client.get(path=self.url)
        assert response_get.status_code == 302, response_get.status_code

        with self.assertLogs(level="WARNING"):
            response_patch = self.client.patch(path=self.url, data={"first_name": "string"})
        assert response_patch.status_code == 405, response_patch.status_code


class TestIsCandidatePermission(APITestCase):
    """Testing IsCandidate class methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user_1 = user_models.User.objects.get(id=1)
        cls.user_2 = user_models.User.objects.get(id=3)
        cls.token_1 = user_services.create_jwttoken(cls.user_1.id)
        cls.token_2 = user_services.create_jwttoken(cls.user_2.id)

        cls.request = APIRequestFactory()
        cls.client = APIClient()
        cls.url = reverse('create_candidate_skill')

        cls.data_1 = {"skill_name": "Python", "level": "BEGINNER", "years_of_experience": 2, "last_used_year": 2024}
        cls.data_2 = {"skill_name": "PyThOn", "level": "BEGINNER", "years_of_experience": -20, "last_used_year": 0}
        
        cls.type_token = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]

    def test_has_object_permission(self):
        """Testing has_object_permission method"""

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_1.access_token}')
        with self.assertLogs(level="WARNING"):
            response_get = self.client.get(path=self.url)
        assert response_get.status_code == 405, response_get.status_code
        
        response_post_1 = self.client.post(path=self.url, data=self.data_1)
        created_skill = models.CandidateSkill.objects.filter(user_id=1).last()
        assert response_post_1.status_code == 201, response_post_1.status_code
        assert self.data_1["skill_name"] == created_skill.skill_name, created_skill
        assert self.data_1["years_of_experience"] == created_skill.years_of_experience, created_skill
        assert self.data_1["last_used_year"] == int(created_skill.last_used_year), created_skill

        response_post_2 = self.client.post(path=self.url, data=self.data_2)
        created_skill = models.CandidateSkill.objects.filter(user_id=1).last()
        assert response_post_2.status_code == 201, response_post_2.status_code
        assert "Python" == created_skill.skill_name, created_skill
        assert 0 == created_skill.years_of_experience, created_skill
        assert 2024 == int(created_skill.last_used_year), created_skill

        self.client.credentials(HTTP_AUTHORIZATION=f'{self.type_token} {self.token_2.access_token}')
        with self.assertLogs(level="WARNING"):
            response_get = self.client.get(path=self.url)
        assert response_get.status_code == 403, response_get.status_code
