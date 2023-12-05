from django.urls import path
from . import views
from .customDecorator import admin_required, anonymous_required

app_name = "Onestop_App"
urlpatterns = [
    path(
        "admin_dashboard/", 
        admin_required(views.dashboard), 
        name='dashboard'
    ),
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
    path(
        "add_faculty/",
        admin_required(views.add_faculty),
        name="add_faculty",
    ),
    path(
        "add_course/",
        admin_required(views.add_course),
        name="add_course",
    ),
    path(
        "add_section/",
        admin_required(views.add_section),
        name="add_section",
    )
]
