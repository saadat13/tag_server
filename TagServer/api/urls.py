from django.urls import path
from .views import ProcessAPIView, PackageProfileAPIView,\
    UserOutputAPIView


urlpatterns = [
    path('processes/', ProcessAPIView.as_view()),
    path('processes/<pid>/package_profiles/', PackageProfileAPIView.as_view()),
    path('outputs/', UserOutputAPIView.as_view()),
]
