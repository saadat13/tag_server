from django.urls import path
from .views import ProcessAPIView, PackageProfileAPIView, UserOutputAPIView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('processes/', ProcessAPIView.as_view()),
    path('processes/<pid>/profiles/', PackageProfileAPIView.as_view()),
    path('outputs/', UserOutputAPIView.as_view()),
]
