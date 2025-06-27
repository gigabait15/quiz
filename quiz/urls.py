from django.urls import path
from . import views

urlpatterns = [
    path('test/<int:pk>/questions/', views.TestQuestionsView.as_view()),
    path('test/<int:pk>/user-answers/', views.TestWithUserAnswersView.as_view()),
    path('answer/', views.SaveAnswerView.as_view()),
    path('submit/<int:test_id>/', views.SubmitTestView.as_view()),
]