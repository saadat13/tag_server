from django.urls import path
from .views import ProcessAPIView, PackageProfileAPIView,\
    UserOutputAPIView
# from .views import block_profile, unblock_profile


urlpatterns = [
    path('processes/', ProcessAPIView.as_view()),
    path('processes/<pid>/package_profiles/', PackageProfileAPIView.as_view()),
    path('outputs/', UserOutputAPIView.as_view()),
    # path('processes/<pid>/package_profiles/<id>/profiles/<i>/block', block_profile),       # block profile when tagging it's content
    # path('processes/<pid>/package_profiles/<id>/profiles/<i>/unblock', unblock_profile),   # unblock profile when cancel tagging
]
