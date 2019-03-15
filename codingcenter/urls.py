from django.urls import path
from codingcenter import views

urlpatterns = [
    path('assignments', views.AssignmentListView.as_view()),
    path('assignments/<pk>', views.AssignmentDetailView.as_view()),
    path('assignments/<pk>/questions', views.AssignmentQuestionsView.as_view()),
    path('questions/<pk>', views.QuestionDetailView.as_view()),
    path('questions', views.QuestionListView.as_view()),
    path('colleges', views.CollegeListView.as_view()),
    path('dashboard', views.DashboardDataView.as_view())
]