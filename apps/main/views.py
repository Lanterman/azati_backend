from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from rest_framework import generics, exceptions, status, decorators, response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from . import models, serializers, permissions, services, db_queries
from apps.user.models import RoleChoice, User


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def get_vacancy_list(request) -> None:
    """Get list of vacancies - endpoint.
       If you are a recruiter - shows all vacancies.
       If you are a candidate - shows suitable vacancies.
    """

    if request.user.role == RoleChoice.CANDIDATE:
        vacancies = services.get_list_of_sorted_vacancies(request.user)
    else:
        vacancies = db_queries.get_vacancies()
    
    serializer = serializers.VacancySerializer(vacancies, many=True)
    return response.Response(serializer.data)


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated, permissions.IsRecruiter])
def create_vacancy_view(request) -> None:
    """Create vacancy - endpoint"""

    vacancy = models.Vacancy.objects.create(owner_id_id=request.user.id)
    return HttpResponseRedirect(redirect_to=vacancy.get_absolute_url())
    

@method_decorator(name="get", decorator=swagger_auto_schema(tags=["vacancies"]))
class VacancyView(generics.RetrieveAPIView):
    """Get avacancy - endpoint"""

    queryset = models.Vacancy.objects.all().prefetch_related("min_skills")
    serializer_class = serializers.VacancySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


@method_decorator(name="post", decorator=swagger_auto_schema(tags=["vacancies"]))
class CreateRecruiterSkillView(generics.CreateAPIView):
    """Create a recruiter skill - endpoint"""

    permission_classes = [IsAuthenticated, permissions.IsRecruiter]
    serializer_class = serializers.CreateRecruiterSkillSerializer

    def post(self, request, *args, **kwargs):
        vacancy = models.Vacancy.objects.filter(id=kwargs["id"])

        if not vacancy:
            raise exceptions.NotFound(detail="This vacancy doesn't exists!", code=status.HTTP_404_NOT_FOUND)

        if vacancy[0].owner_id != request.user:
            raise exceptions.PermissionDenied(detail="You don't have access!", code=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(vacancy_id_id=self.kwargs["id"])


@method_decorator(name="post", decorator=swagger_auto_schema(tags=["candidates"]))
class CreateCandidateSkillView(generics.CreateAPIView):
    """Create a candidate skill - endpoint"""

    permission_classes = [IsAuthenticated, permissions.IsCandidate]
    serializer_class = serializers.CreateCandidateSkillSerializer
    
    def perform_create(self, serializer):
        serializer.save(user_id_id=self.request.user.id)


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def get_candidate_list(request, vacancy_id) -> None:
    """Get list of candidates - endpoint.
       If you are a candidate - shows all vacancies.
       If you are a recruiter - shows suitable vacancies.
    """

    if request.user.role == RoleChoice.RECRUITER:
        candidates = services.get_list_of_sorted_candidates(vacancy_id)
    else:
        candidates = db_queries.get_candidates()
    
    serializer = serializers.CandidateSerializer(candidates, many=True)
    return response.Response(serializer.data)

@method_decorator(name="get", decorator=swagger_auto_schema(tags=["candidates"]))
class CandidateView(generics.RetrieveAPIView):
    """Get candidate - endpoint"""

    queryset = User.objects.all().prefetch_related("skills")
    serializer_class = serializers.CandidateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"
