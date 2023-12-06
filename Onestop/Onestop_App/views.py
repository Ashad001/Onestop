from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AdministrationLoginForm, StudentForm, FacultyForm,CourseForm,SectionForm, StudentLoginForm, TicketForm, ResponseForm
from django.contrib import messages
from django import forms
from .models import Ticket, Notification, User
from .chatbot import process_begin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    if request.method == "POST":
        student = request.user.student  # Assuming the user is authenticated
        ticket_Form = TicketForm(request.POST, instance=Ticket(student=student))
        if ticket_Form.is_valid():
            try:
                ticket_Form.save()
                messages.success(request, "Query successfully created")
            except forms.ValidationError as e:
                messages.error(request, "Integrity Error: " + str(e))
            
            return render(
                request,
                "Onestop_App/create_query.html",
                {"ticket_Form": TicketForm(instance=Ticket(student=student))},
            )
        else:
            print(ticket_Form.errors)
            messages.error(request, "Something is not quite right (。_。)")
            return render(
                request,
                "Onestop_App/create_query.html",
                {"ticket_Form": ticket_Form},
            )
    else:
        return render(
            request,
            "Onestop_App/create_query.html",
            {"ticket_Form": TicketForm()},
        )

def query_status(request):
    student = request.user.student
    tickets = Ticket.objects.filter(student=student)
    
    return render(
        request,
        "Onestop_App/query_status.html",
        {"tickets": tickets},
    )

def student_timetable(request):
    return render(
        request,
        "Onestop_App/student_timetable.html",
    )

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

def admin_queries(request):
    all_tickets = Ticket.objects.all()
    tickets_per_page = 10
    paginator = Paginator(all_tickets, tickets_per_page)
    page = request.GET.get('page')

    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    return render(
        request,
        "Onestop_App/admin_queries.html",
        {"tickets": tickets},
    )

def admin_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            ticket.admin_response = form.cleaned_data['admin_response']
            ticket.status = form.cleaned_data['status']
            ticket.save()

            if form.cleaned_data['notification']:
                create_notification(ticket.student, f"Your ticket has a new response with request for {ticket.service}.")

            return redirect('Onestop_App:admin_queries')
    else:
        form = ResponseForm()

    return render(
        request,
        'Onestop_App/admin_response_form.html',
        {'ticket': ticket, 'form': form}
    )

def create_notification(student, content):
    # Access the associated User instance through the student
    user = student.user

    Notification.objects.create(
        user=user,
        notification_content=content,
        is_read=False,
    )

def admin_notifications(request):
    user_haseeb = User.objects.get(username='haseeb')

    # Filter notifications for the specified user
    notifications = Notification.objects.filter(user=user_haseeb).order_by('-timestamp')

    return render(request, 'Onestop_App/admin_notifications.html', {'notifications': notifications})

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.mark_as_read()

    # Assuming your Ticket model has a ForeignKey to Notification, adjust this part accordingly
    ticket_id = notification.ticket.id  # Replace 'ticket' with the actual ForeignKey name in your Notification model

    return redirect('Onestop_App:ticket_detail', ticket_id=ticket_id)

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'Onestop_App/ticket_detail.html', {'ticket': ticket})