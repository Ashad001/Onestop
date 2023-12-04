from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Section)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(Appointment)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(Ticket)
