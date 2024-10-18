from rest_framework import serializers

from . import models
from apps.user.models import User


class RecruiterSkillSerializer(serializers.ModelSerializer):
    """A recruiter skill serializer"""

    class Meta:
        model = models.RecruiterSkill
        fields = ["id", "skill_name", "min_level", "min_years_of_experience"]


class CandidateSkillSerializer(serializers.ModelSerializer):
    """A candidate skill serializer"""

    class Meta:
        model = models.CandidateSkill
        fields = ["id", "skill_name", "level", "years_of_experience", "last_used_year"]


class VacancySerializer(serializers.ModelSerializer):
    """A vacancy serializer"""

    min_skills = RecruiterSkillSerializer(many=True)

    class Meta:
        model = models.Vacancy
        fields = ["id", "owner_id", "min_skills"]


class CreateRecruiterSkillSerializer(serializers.ModelSerializer):
    """Create recruiter skill serializer"""

    class Meta:
        model = models.RecruiterSkill
        fields = ["skill_name", "min_level", "min_years_of_experience"]
    
    def validate_min_years_of_experience(self, value: int) -> int:
        return value if 0 < value < 100 else 0


class CreateCandidateSkillSerializer(serializers.ModelSerializer):
    """Create candidate skill serializer"""

    class Meta:
        model = models.CandidateSkill
        fields = ["skill_name", "level", "years_of_experience", "last_used_year"]
    
    def validate_years_of_experience(self, value: int) -> int:
        return value if 0 < value < 100 else 0
    
    def validate_last_used_year(self, value: int) -> int:
        return value if 2000 < value < 2024 else 2024


class CandidateSerializer(serializers.ModelSerializer):
    """A candidate serializer"""

    skills = CandidateSkillSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "skills"]
