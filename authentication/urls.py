from django.urls import path, re_path

from authentication.controller.index_view import IndexView
from authentication.controller.login_view import LoginView
from authentication.controller.logout_view import LogoutView
from authentication.controller.me_view import MeView
from authentication.controller.signup_view import SignupView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('me', MeView.as_view()),
]