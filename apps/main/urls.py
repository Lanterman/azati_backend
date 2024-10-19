from django.urls import path

from . import views

urlpatterns = [
    path('vacancies/', views.get_vacancy_list, name='vacancy-list'),
    path('vacancies/create_vacancy', views.create_vacancy_view, name='create_vacancy'),
    path('vacancies/<int:id>/', views.VacancyView.as_view(), name='vacancy-detail'),
    path('vacancies/<int:id>/create_min_skill/', views.CreateRecruiterSkillView.as_view(), name='create_recruiter_skill'),
    path('candidates/create_skill/', views.CreateCandidateSkillView.as_view(), name='create_candidate_skill'),
    path('candidates/show/<int:vacancy_id>/', views.get_candidate_list, name='candidate-list'),
    path('candidates/<str:username>/', views.CandidateView.as_view(), name='candidate-detail'),
]