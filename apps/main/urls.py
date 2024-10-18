from django.urls import path

from . import views

urlpatterns = [
    path('vacancies/', views.VacancyListView.as_view(), name='vacancy-list'),
    path('vacancies/create_vacancy', views.create_vacancy_view, name='create_vacancy'),
    path('vacancies/<int:id>/', views.VacancyView.as_view(), name='vacancy-detail'),
    path('vacancies/<int:id>/create_min_skill/', views.CreateRecruiterSkillView.as_view(), name='create_recruiter_skill'),
    path('candidate/create_skill/', views.CreateCandidateSkillView.as_view(), name='create_candidate_skill'),
    path('candidates/', views.CandidateListView.as_view(), name='candidate-list'),
]