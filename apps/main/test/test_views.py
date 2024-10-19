import json

from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from apps.user.auth import models as auth_models


class TestGetVacancyList(APITestCase):
    """Testing the get_vacancy_list endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_2 = auth_models.JWTToken.objects.get(id=6)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)

        cls.client = APIClient()

        cls.path = reverse("vacancy-list")

    def test_get_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.get(self.path)
        list_vacancy_id = [vacancy["id"] for vacancy in response.data]
        assert 200 == response.status_code, response.status_code
        assert 7 == len(response.data), len(response.data)
        assert [3, 5, 2, 6, 9, 7, 1] == list_vacancy_id, list_vacancy_id

        # Candidate_2 - token_2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_2.access_token)
        response = self.client.get(self.path)
        list_vacancy_id = [vacancy["id"] for vacancy in response.data]
        assert 200 == response.status_code, response.status_code
        assert 9 == len(response.data), len(response.data)
        assert [2, 5, 6, 9, 3, 1, 8, 7, 4] == list_vacancy_id, list_vacancy_id

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.get(self.path)
        list_vacancy_id = [vacancy["id"] for vacancy in response.data]
        assert 200 == response.status_code, response.status_code
        assert 9 == len(response.data), len(response.data)
        assert [1, 2, 3, 4, 5, 6, 7, 8, 9] == list_vacancy_id, list_vacancy_id

    
    def test_post_method(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error


class TestCreateVacancyView(APITestCase):
    """Testing the create_vacancy_view endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)

        cls.client = APIClient()

        cls.path = reverse("create_vacancy")
    
    def test_post_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'This action is only allowed for recruiters.'
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error
    
    def test_get_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'This action is only allowed for recruiters.'
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.get(self.path)
        assert 302 == response.status_code, response.status_code


class TestVacancyView(APITestCase):
    """Testing the VacancyView endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)

        cls.client = APIClient()

        cls.path_1 = reverse("vacancy-detail", kwargs={"id": 1})
        cls.path_2 = reverse("vacancy-detail", kwargs={"id": 2})
    
    def test_post_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error
    
    def test_get_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.get(self.path_1)
        assert 200 == response.status_code, response.status_code
        assert 1 == response.data["id"], response.data["id"]
        assert 4 == response.data["owner_id"], response.data["owner_id"]

        response = self.client.get(self.path_2)
        assert 200 == response.status_code, response.status_code
        assert 2 == response.data["id"], response.data["id"]
        assert 3 == response.data["owner_id"], response.data["owner_id"]

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.get(self.path_1)
        assert 200 == response.status_code, response.status_code
        assert 1 == response.data["id"], response.data["id"]
        assert 4 == response.data["owner_id"], response.data["owner_id"]


class TestCreateRecruiterSkillView(APITestCase):
    """Testing the CreateRecruiterSkillView endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)
        cls.token_4 = auth_models.JWTToken.objects.get(id=4)

        cls.client = APIClient()

        cls.data_1 = {"skill_name": "Python", "min_level": "BEGINNER", "min_years_of_experience": 5}
        cls.data_2 = {"skill_name": "PytHoN", "min_level": "BEGINNER", "min_years_of_experience": 1012}

        cls.path_1 = reverse("create_recruiter_skill", kwargs={"id": 1})
        cls.path_2 = reverse("create_recruiter_skill", kwargs={"id": 20})
    
    def test_get_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'This action is only allowed for recruiters.'
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "GET" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error
    
    def test_post_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'This action is only allowed for recruiters.'
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        ## 403 "You don't have access!"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.post(self.path_1, data=self.data_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = "You don't have access!"
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        ## 404 "This vacancy doesn't exists!"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.post(self.path_2, data=self.data_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = "This vacancy doesn't exists!"
        assert 404 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        ## valid data_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_4.access_token)
        response = self.client.post(self.path_1, data=self.data_1)
        assert 201 == response.status_code, response.status_code
        assert self.data_1 == response.data, response.data

        ## valid data_2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_4.access_token)
        response = self.client.post(self.path_1, data=self.data_2)
        assert 201 == response.status_code, response.status_code
        assert self.data_2 != response.data, response.data
        assert {'skill_name': 'Python', 'min_level': 'BEGINNER', 'min_years_of_experience': 0} == response.data, response.data


class TestCreateCandidateSkillView(APITestCase):
    """Testing the CreateCandidateSkillView endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)

        cls.client = APIClient()

        cls.data_1 = {"skill_name": "Python", "level": "BEGINNER", 
                      "years_of_experience": 5, "last_used_year": 2020}
        
        cls.data_2 = {"skill_name": "PyTHon", "level": "BEGINNER", 
                      "years_of_experience": 121, "last_used_year": -20}

        cls.path = reverse("create_candidate_skill")
    
    def test_get_method(self):
        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'This action is only allowed for candidates.'
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.get(self.path)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "GET" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error
    
    def test_post_method(self):
        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path, data=self.data_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'This action is only allowed for candidates.'
        assert 403 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Candidate_1 - token_1
        # Validate data_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.post(self.path, data=self.data_1)
        assert 201 == response.status_code, response.status_code
        assert self.data_1 == response.data, response.data

        # Validate data_2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.post(self.path, data=self.data_2)
        assert 201 == response.status_code, response.status_code
        assert {'skill_name': 'Python', 'level': 'BEGINNER', 
                'years_of_experience': 0, 'last_used_year': 2024} == response.data, response.data


class TestGetCandidateList(APITestCase):
    """Testing the get_candidate_list endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)
        cls.token_4 = auth_models.JWTToken.objects.get(id=4)

        cls.client = APIClient()

        cls.path_1 = reverse("candidate-list", kwargs={"vacancy_id": 1})
        cls.path_2 = reverse("candidate-list", kwargs={"vacancy_id": 2})

    def test_get_method(self):
        # Vacancy 1
        ## Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.get(self.path_1)
        list_candidate_id = [candidate["id"] for candidate in response.data]
        assert 200 == response.status_code, response.status_code
        assert 6 == len(response.data), len(response.data)
        assert [6, 7, 2, 1, 5, 4] == list_candidate_id, list_candidate_id

        ## Recruiter - token_4
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_4.access_token)
        response = self.client.get(self.path_1)
        list_candidate_id = [candidate["id"] for candidate in response.data]
        assert 200 == response.status_code, response.status_code
        assert 6 == len(response.data), len(response.data)
        assert [6, 7, 2, 1, 5, 4] == list_candidate_id, list_candidate_id

        ## Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.get(self.path_1)
        list_candidate_id = [candidate["id"] for candidate in response.data]
        assert 200 == response.status_code, response.status_code
        assert 5 == len(response.data), len(response.data)
        assert [1, 2, 5, 6, 7] == list_candidate_id, list_candidate_id

        # Vacancy 2
        ## Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.get(self.path_2)
        list_candidate_id = [candidate["id"] for candidate in response.data]
        assert 200 == response.status_code, response.status_code
        assert 6 == len(response.data), len(response.data)
        assert [6, 7, 2, 4, 1, 5] == list_candidate_id, list_candidate_id

        ## Recruiter - token_4
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_4.access_token)
        response = self.client.get(self.path_2)
        list_candidate_id = [candidate["id"] for candidate in response.data]
        assert 200 == response.status_code, response.status_code
        assert 6 == len(response.data), len(response.data)
        assert [6, 7, 2, 4, 1, 5] == list_candidate_id, list_candidate_id

        ## Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.get(self.path_2)
        list_candidate_id = [candidate["id"] for candidate in response.data]
        assert 200 == response.status_code, response.status_code
        assert 5 == len(response.data), len(response.data)
        assert [1, 2, 5, 6, 7] == list_candidate_id, list_candidate_id
    
    def test_post_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error


class TestCandidateView(APITestCase):
    """Testing the CandidateView endpoint methods"""

    fixtures = ["./config/test/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.token_1 = auth_models.JWTToken.objects.get(id=1)
        cls.token_3 = auth_models.JWTToken.objects.get(id=3)

        cls.client = APIClient()

        cls.path_1 = reverse("candidate-detail", kwargs={"username": "lanterman"})
        cls.path_2 = reverse("candidate-detail", kwargs={"username": "recruiter"})
    
    def test_post_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        with self.assertLogs(level="WARNING"):
            response = self.client.post(self.path_1)
        detail_error = json.loads(response.content)["detail"]
        test_detail_error = 'Method "POST" not allowed.'
        assert 405 == response.status_code, response.status_code
        assert test_detail_error == detail_error, detail_error
    
    def test_get_method(self):
        # Candidate_1 - token_1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_1.access_token)
        response = self.client.get(self.path_1)
        assert 200 == response.status_code, response.status_code
        assert 1 == response.data["id"], response.data["id"]

        response = self.client.get(self.path_2)
        assert 200 == response.status_code, response.status_code
        assert 3 == response.data["id"], response.data["id"]

        # Recruiter - token_3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_3.access_token)
        response = self.client.get(self.path_1)
        assert 200 == response.status_code, response.status_code
        assert 1 == response.data["id"], response.data["id"]

        response = self.client.get(self.path_2)
        assert 200 == response.status_code, response.status_code
        assert 3 == response.data["id"], response.data["id"]
