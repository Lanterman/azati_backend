from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from config import settings


User = settings.AUTH_USER_MODEL


class LevelChoice(models.TextChoices):
    """Choose level"""

    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class Vacancy(models.Model):
    """A vacancy model"""

    owner_id: int = models.ForeignKey(to=User, verbose_name=_("owner"), on_delete=models.CASCADE, related_name="vacancies")

    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancies")

    def __str__(self):
        return f"Vacancy {self.id}"
    
    def get_absolute_url(self):
        return reverse('vacancy-detail', kwargs={'id': self.id})


class CandidateSkill(models.Model):
    """A candidate skill model"""

    skill_name: str = models.CharField(_("skill name"), max_length=50)
    level: str = models.CharField(_("level"), max_length=30, default=LevelChoice.BEGINNER,  choices=LevelChoice.choices)
    years_of_experience: int = models.IntegerField(_("years_of_experience"))
    last_used_year: int = models.IntegerField(_("last_used_year"), default=2024)
    user_id: int = models.ForeignKey(to=User, verbose_name=_("user"), on_delete=models.CASCADE, related_name="skills")

    class Meta:
        verbose_name = _("CandidateSkill")
        verbose_name_plural = _("CandidateSkills")

    def __str__(self):
        return f"{self.skill_name} - {self.years_of_experience} years of experience"


class RecruiterSkill(models.Model):
    """A recruiter skill model"""

    skill_name: str = models.CharField(_("skill name"), max_length=50)
    min_level: str = models.CharField(_("minimal level"), max_length=30, default=LevelChoice.BEGINNER,  
                                      choices=LevelChoice.choices)
    min_years_of_experience: int = models.IntegerField(_("minimal_years_of_experience"))
    vacancy_id: int = models.ForeignKey(to=Vacancy, verbose_name=_("vacancy"), on_delete=models.CASCADE, 
                                        related_name="min_skills")

    class Meta:
        verbose_name = _("RecruiterSkill")
        verbose_name_plural = _("RecruiterSkills")

    def __str__(self):
        return f"{self.skill_name} - {self.min_years_of_experience} minimal years of experience"
