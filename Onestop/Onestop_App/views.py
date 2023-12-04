from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AdministrationLoginForm, StudentForm
from django.contrib import messages
from django import forms
# Create your views here.


def page_not_found_404(request, exception, message=None):
    return render(
        request,
        "Onestop_App/page_not_found_404.html",
        {"message": message},
        status=404,
    )


def dashboard(request):
    return render(
        request,
        "Onestop_App/admin_dashboard.html"
    )


def admin_login(request):
    if request.method == "POST":
        login_form = AdministrationLoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect("Onestop_App:dashboard")
            else:
                messages.error(request, "Invalid username and/or password.")
                return render(
                    request,
                    "Onestop_App/admin_login.html",
                    {
                        "login_form": login_form,
                    },
                )
        else:
            messages.error(
                request, "Invalid email and/or password or submission.")
            return render(
                request,
                "Onestop_App/admin_login.html",
                {"login_form": login_form},
            )
    else:
        if request.user.is_authenticated:
            return redirect("Onestop_App:dashboard")
        else:
            return render(
                request,
                "Onestop_App/admin_login.html",
                {"login_form": AdministrationLoginForm()},
            )


def admin_logout(request):
    logout(request)
    return redirect("Onestop_App:admin_login")


def add_student(request):
    if request.method == "POST":
        student_Form = StudentForm(request.POST)
        if student_Form.is_valid():
            try:
                student_Form.save()
                messages.success(
                    request, "Student profile successfully created"
                )
            except forms.ValidationError as e:
                messages.error(request, "Integrity Error " + str(e))

            return render(
                request,
                "Onestop_App/add_student.html",
                {"student_Form": StudentForm(), },
            )
        else:
            # print(instanceForm.errors)
            messages.error(request, "Something is not quiite right (。_。)")

            return render(
                request,
                "Onestop_App/add_student.html",
                {"student_Form": student_Form, },
            )
    else:
        return render(
            request,
            "Onestop_App/add_student.html",
            {"student_Form": StudentForm(), },
        )
