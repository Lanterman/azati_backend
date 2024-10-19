from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from apps.main import serializers


class TestCreateRecruiterSkillSerializer(APITestCase):
    """Testing CreateRecruiterSkillSerializer class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.CreateRecruiterSkillSerializer()
    
    def test_validate_skill_name(self):
        """Testing validate_skill_name method"""

        response = self.instance.validate_skill_name("Python")
        assert "Python" == response, response

        response = self.instance.validate_skill_name("PytHon")
        assert "Python" == response, response

        response = self.instance.validate_skill_name("python")
        assert "Python" == response, response

        
    def test_validate_min_years_of_experience(self):
        """Testing validate_min_years_of_experience method"""

        response = self.instance.validate_min_years_of_experience(-1)
        assert 0 == response, response

        response = self.instance.validate_min_years_of_experience(33)
        assert 33 == response, response

        response = self.instance.validate_min_years_of_experience(101)
        assert 0 == response, response


class TestCreateCandidateSkillSerializer(APITestCase):
    """Testing CreateCandidateSkillSerializer class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.instance = serializers.CreateCandidateSkillSerializer()
    
    def test_validate_skill_name(self):
        """Testing validate_skill_name method"""

        response = self.instance.validate_skill_name("Python")
        assert "Python" == response, response

        response = self.instance.validate_skill_name("PytHon")
        assert "Python" == response, response

        response = self.instance.validate_skill_name("python")
        assert "Python" == response, response

    def test_validate_years_of_experience(self):
        """Testing validate_years_of_experience method"""

        response = self.instance.validate_years_of_experience(-1)
        assert 0 == response, response

        response = self.instance.validate_years_of_experience(33)
        assert 33 == response, response

        response = self.instance.validate_years_of_experience(101)
        assert 0 == response, response
    
    def test_validate_last_used_year(self):
        """Testing validate_last_used_year method"""

        response = self.instance.validate_last_used_year(1999)
        assert 2024 == response, response

        response = self.instance.validate_last_used_year(2021)
        assert 2021 == response, response

        response = self.instance.validate_last_used_year(2025)
        assert 2024 == response, response
