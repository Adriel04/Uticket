from django.urls import path

from . import views
from .views import SignUpView

urlpatterns = [
    path("<int:user_id>/", views.user_panel, name="panel"),
    path("<int:user_id>/recharge/", views.recharge, name="recharge"),
    path("signup/", SignUpView.as_view(), name="signup"),
]