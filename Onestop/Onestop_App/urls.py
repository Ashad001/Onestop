from django.urls import path
from . import views
from .customDecorator import admin_required, anonymous_required,normal_user_required
from django.contrib.auth.decorators import login_required

app_name = "Onestop_App"
urlpatterns = [
    path(
        "",
        views.student_login,
        name = "student_login"
    ),
    path(
        "create_query/",
        login_required(views.create_query),
        name = "create_query"
    ),
    path(
        "query_status/",
        login_required(views.query_status),
        name = "query_status"
    ),
    path(
        "student_timetabe/",
        login_required(views.student_timetable),
        name = "student_timetable"
    ),
    path(
        "student_faq/",
        login_required(views.student_faq),
        name = "student_faq"
    ),
    path(
        "student_dashboard/",
        login_required(views.student_dashboard),
        name = "student_dashboard"
    ),
    path(
        "student_logout/",
        login_required(views.student_logout),
        name="student_logout",
    ),
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
