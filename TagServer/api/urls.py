from django.urls import path
from .views import ProcessAPIView, PackageProfileAPIView, UserOutputAPIView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('processes/', ProcessAPIView.as_view()),
    path('processes/<pid>/profiles/', PackageProfileAPIView.as_view()),
    path('outputs/', UserOutputAPIView.as_view()),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
