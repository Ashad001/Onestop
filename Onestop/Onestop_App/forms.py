from django import forms
from django.core.exceptions import ValidationError
from Onestop_App.models import User, Student, Faculty
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AdministrationLoginForm(AuthenticationForm):
    """
    It's just an authentication form.
    """
    pass