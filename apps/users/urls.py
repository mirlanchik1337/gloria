from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .ruters import MyRouter
router = DefaultRouter()
# my_router = MyRouter()
# регистрация
router.register(r"register", views.UserRegistrationViewSet,
                basename='register')
# логин
router.register(r"login", views.UserLoginViewSet,
                basename="login")
# подтверждение номера
router.register(r"confirm-user", views.UserConfirmViewSet,
                basename="confirm-user")
# выход из аккаунта
router.register(r"logout", views.LogoutViewSet,
                basename="logout")
# создание кода для востановления
router.register(r"reset-password-phone-number", views.PasswordResetSearchUserViewSet,
                basename="reset-password-phone-number")
# подтверждение кода
router.register(r"reset-password-code", views.PasswordResetTokenViewSet,
                basename="reset-password-code")
# создание нового пароля + code
# router.register(r"reset-new-password/<int:token>", views.PasswordResetNewPasswordViewSet,
#                 basename="reset-new-password-with-code")
# профиль
router.register(r"profile", views.ProfileViewSet,
                basename="profile")

urlpatterns = [
    *router.urls,
    # path("register/", views.UserRegistrationView.as_view(), name="user-registration"),
    # path("login/", views.UserLoginUserAPIView.as_view(), name="user-authorization"),
    # path("confirm-user/", views.UserConfirmAPIView.as_view(), name="user-confirm"),
    # path("logout/", views.LogoutAPIView.as_view(), name="user-logout"),
    # # создание кода для востановления
    # path(
    #     "reset-password-phone-number/",
    #     views.PasswordResetSearchUserAPIView.as_view(),
    #     name="search user and generate code",
    # ),
    # # подтверждение кода
    # path(
    #     "reset-password-code/",
    #     views.PasswordResetTokenAPIView.as_view(),
    #     name="code",
    # ),
    # # создание нового пароля + code
    path(
        "reset-new-password/< int:code>/",
        views.PasswordResetNewPasswordViewSet.as_view(),
        name="new-password",
    ),
    path("set-password/", views.SetPassword.as_view())
    # path("profile/", views.ProfileAPIView.as_view(), name="profile-list"),
    # path("profile/<str:id>/", views.ProfileDetailAPIView.as_view(), name="profile-update,delete"),
]
