from django.urls import path
from rest_framework.authtoken import views as AuthTokenView

from . import views

urlpatterns = [
    path("create-user/", views.CreateUserApiView.as_view()),
    path("login/", AuthTokenView.obtain_auth_token),
    path("donner-list/", views.BloodDonnerListAPIView.as_view()),
    path("user/<str:email>/update/", views.UserProfileUpdateAPIView.as_view()),
    path("blood-needed-list/", views.BloodNeededListAPIView.as_view()),
    path("blood-donate-add/", views.UserBloodDonateAPIView.as_view()),
    path(
        "donner-list/<str:email>/donation-list/",
        views.BloodDonnerDonateListView.as_view(),
    ),
    path("blood-need-create/", views.BloodNeededCreateAPIView.as_view()),
    path(
        "blood-need-update/<int:id>/",
        views.BloodNeededUpdateAPIView.as_view(),
    ),
    path("user-device-token/", views.DeviceTokenAPIView.as_view()),
]
