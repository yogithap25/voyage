from django import forms
from django.contrib.auth.models import User

from .models import Booking


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "name",
            "email",
            "mobile",
            "check_in",
            "check_out",
        ]