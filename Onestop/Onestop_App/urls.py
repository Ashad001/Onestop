from django.urls import path
from . import views
from .customDecorator import admin_required, anonymous_required

app_name = "Onestop_App"
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path(
        "admin_login/",
        anonymous_required(views.admin_login),
        name="admin_login",
    ),
    path(
        "admin_logout/",
        admin_required(views.admin_logout),
        name="admin_logout",
    ),
    path(
        "add_student/",
        admin_required(views.add_student),
        name="add_student",
    ),
]
