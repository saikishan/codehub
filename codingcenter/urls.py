from django.urls import path
from codingcenter import views

urlpatterns = [
    path('assignments/', views.AssignmentListView.as_view()),
]