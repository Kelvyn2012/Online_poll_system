from django.urls import path
from .views import PollCreateView, VoteCreateView, PollResultView, PollListView
from . import views

urlpatterns = [
    path("", views.home),
    path("polls/", PollCreateView.as_view()),
    path("vote/", VoteCreateView.as_view()),
    path("polls/<int:pk>/results/", PollResultView.as_view()),
    path("polls/list/", PollListView.as_view()),
]
