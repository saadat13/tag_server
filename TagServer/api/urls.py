from django.urls import path
from .views import ProcessListAPIView, ProcessAPIView, ProfileListAPIView, UserOutputAPIView


urlpatterns = [
    path('processes/', ProcessListAPIView.as_view()),
    path('processes/<int:pk>/', ProcessAPIView.as_view()),
    path('processes/<int:pk>/profiles/', ProfileListAPIView.as_view()),
    path('outputs/', UserOutputAPIView.as_view()),
]
