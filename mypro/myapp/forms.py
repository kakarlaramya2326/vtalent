import re
from datetime import date

from django import forms


class StudentRegistrationForm(forms.Form):
    student_name = forms.CharField(
        label="Student Name",
        max_length=100,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "name",
                "placeholder": "Enter your full name",
            }
        ),
    )
    college_name = forms.CharField(
        label="College Name",
        max_length=150,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "organization",
                "placeholder": "Enter your college name",
            }
        ),
    )
    mobile_number = forms.CharField(
        label="Mobile Number",
        max_length=10,
        min_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "tel",
                "inputmode": "numeric",
                "autocomplete": "tel-national",
                "pattern": "[0-9]{10}",
                "placeholder": "10-digit mobile number",
            }
        ),
        error_messages={
            "min_length": "Enter exactly 10 digits.",
            "max_length": "Enter exactly 10 digits.",
        },
    )
    passed_out_year = forms.IntegerField(
        label="Passed Out Year",
        min_value=1950,
        max_value=date.today().year,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "1950",
                "max": str(date.today().year),
                "placeholder": "e.g. 2026",
            }
        ),
        error_messages={
            "invalid": "Enter a valid four-digit year.",
            "min_value": "Enter a valid passed out year.",
            "max_value": "Passed out year cannot be in the future.",
        },
    )

    def clean_student_name(self):
        name = self.cleaned_data["student_name"]
        if not re.fullmatch(r"[^\W\d_]+(?:[ .'-][^\W\d_]+)*\.?", name):
            raise forms.ValidationError(
                "Enter a valid name using letters, spaces, apostrophes, or hyphens."
            )
        return name

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data["mobile_number"]
        if not re.fullmatch(r"[0-9]{10}", mobile_number):
            raise forms.ValidationError("Enter exactly 10 digits.")
        return mobile_number
