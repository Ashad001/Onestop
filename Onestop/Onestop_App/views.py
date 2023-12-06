from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AdministrationLoginForm, StudentForm, FacultyForm,CourseForm,SectionForm, StudentLoginForm
from django.contrib import messages
from django import forms
from .chatbot import process_begin

# Create your views here.

def page_not_found_404(request, exception, message=None):
    return render(
        request,
        "Onestop_App/page_not_found_404.html",
        {"message": message},
        status=404,
    )
    
def student_dashboard(request):
    return render(
        request,
        "Onestop_App/student_dashboard.html",
    )


def create_query(request):
    return HttpResponse("Create Query")

def query_status(request):
    return HttpResponse("Query Response")

def student_timetable(request):
    return HttpResponse("Timetable")

def student_faq(request):
    return HttpResponse("Student FAQ")


def dashboard(request):
    return render(
        request,
        "Onestop_App/admin_dashboard.html"
    )

def student_login(request):
    if request.method == "POST":
        login_form = StudentLoginForm(request,data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)
                print("hjhkj")
                return redirect("Onestop_App:student_dashboard")
            else:
                messages.error(request, "Invalid username and/or password.")
                return render(
                    request,
                    "Onestop_App/student_login.html",
                    {
                        "login_form": login_form,
                    },
                )
        else:
            messages.error(
                request, "Invalid email and/or password or submission.")
            return render(
                request,
                "Onestop_App/student_login.html",
                {"login_form": login_form},
            )
    else:
        if request.user.is_authenticated:
            return redirect("Onestop_App:student_dashboard")
        else:
            return render(
                request,
                "Onestop_App/student_login.html",
                {"login_form":StudentLoginForm()},
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

def student_logout(request):
    logout(request)
    return redirect("Onestop_App:student_login")


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


def add_faculty(request):
    if request.method == "POST":
        faculty_Form = FacultyForm(request.POST)
        if faculty_Form.is_valid():
            try:
                faculty_Form.save()
                messages.success(
                    request, "Faculty profile successfully created"
                )
            except forms.ValidationError as e:
                messages.error(request, "Integrity Error: " + str(e))

            return render(
                request,
                "Onestop_App/add_faculty.html",
                {"faculty_Form": FacultyForm(), },
            )
        else:
            messages.error(request, "Something is not quite right (。_。)")
            
            return render(
                request,
                "Onestop_App/add_faculty.html",
                {"faculty_Form": FacultyForm(), },
            )
    else:
        return render(
            request,
            "Onestop_App/add_faculty.html",
            {"faculty_Form": FacultyForm(),},
        )
    
def add_course(request):
    if request.method=="POST":
        course_Form = CourseForm(request.POST)
        if course_Form.is_valid():
            try:
                course_Form.save()
                messages.success(
                    request, "Course successfully created"
                )
            except forms.ValidationError as e:
                messages.error(request, "Integrity Error: " + str(e))
            
            return render(
                request,
                "Onestop_App/add_course.html",
                {"course_Form": CourseForm(), },
            )
        else:
            messages.error(request, "Something is not quite right (。_。)")
            
            return render(
                request,
                "Onestop_App/add_course.html",
                {"course_Form": CourseForm(), },
            )
    else:
        return render(
            request,
            "Onestop_App/add_course.html",
            {"course_Form": CourseForm(), },
        )
        
def add_section(request):
    if request.method=="POST":
        section_Form = SectionForm(request.POST) 
        if section_Form.is_valid():
            try:
                section_Form.save()
                messages.success(
                    request, "Section successfully created"
                )
            except forms.ValidationError as e:
                messages.error(request, "Integrity Error: " + str(e))
            
            return render(
                request,
                "Onestop_App/add_section.html",
                {"section_Form": SectionForm(), },
            )
        else:
            messages.error(request, "Something is not quite right (。_。)")
            
            return render(
                request,
                "Onestop_App/add_section.html",
                {"section_Form": SectionForm(), },
            )
    else:
        return render(
            request,
            "Onestop_App/add_section.html",
            {"section_Form": SectionForm(), },
        )
            
def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input', '')
        result = process_begin(user_input)
        response_data = {'result': result}
        return JsonResponse(response_data)

    return render(request, "Onestop_App/chatbot.html")