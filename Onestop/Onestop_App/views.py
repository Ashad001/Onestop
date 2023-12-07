from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AdministrationLoginForm, StudentForm, FacultyForm,CourseForm,SectionForm, StudentLoginForm, TicketForm, ResponseForm,AppointmentForm,ChangeAppointmentStatusForm
from django.contrib import messages
from django import forms
from .models import Ticket, Notification, User
from .chatbot import process_begin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Appointment

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

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def add_student(request):
    if request.method == "POST":
        student_Form = StudentForm(request.POST)
        if student_Form.is_valid():
            try:
                student = student_Form.save()
                send_student_creation_email(student)
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
            messages.error(request, "Something is not quite right (。_。)")

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

def send_student_creation_email(student):
    subject = 'Welcome to OneStop App'
    recipient_email = student.user.email
    context = {'username': student.user.username, 'password': student.user.password}  # Replace '*****' with the actual password

    # Pass context as the second argument to render_to_string
    html_message = render_to_string('Onestop_App/email_welcome.html', context)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(subject, plain_message, 'digitalized.onestop@gmail.com', [recipient_email], html_message=html_message)


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

def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'Onestop_App/student_notifications.html', {'notifications': notifications})

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.mark_as_read()

    ticket_id = notification.ticket.id

    return redirect('Onestop_App:ticket_detail', ticket_id=ticket_id)

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'Onestop_App/ticket_detail.html', {'ticket': ticket})

def ticket_det(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'Onestop_App/ticket_det.html', {'ticket': ticket})

def schedule_appointment(request):
    if request.method == 'POST':
        appointment_Form = AppointmentForm(request.POST)
        if appointment_Form.is_valid():
            appointment = appointment_Form.save(commit=False)
            appointment.student = request.user.student
            appointment.status = 'submitted'
            appointment.appointment_date = appointment_Form.cleaned_data['appointment_date']
            appointment.save()
            
            messages.success(request, 'Appointment scheduled successfully.')
            return redirect('Onestop_App:student_dashboard')
    else:
        appointment_Form = AppointmentForm()

    return render(request, 'Onestop_App/schedule_appointment.html', {'appointment_Form': appointment_Form})

def all_appointments(request):
    appointments = Appointment.objects.all()

    return render(request, 'Onestop_App/all_appointments.html', {'appointments': appointments})

def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    return render(request, 'Onestop_App/appointment_detail.html', {'appointment': appointment})

def change_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = ChangeAppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment status changed successfully.')
            return redirect('Onestop_App:admin_notifications')
    else:
        form = ChangeAppointmentStatusForm(instance=appointment)

    return render(request, 'Onestop_App/change_appointment_status.html', {'form': form, 'appointment': appointment})