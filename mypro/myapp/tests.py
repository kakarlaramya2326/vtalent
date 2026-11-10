from datetime import date
from urllib.parse import parse_qs, urlsplit

from django.test import TestCase
from django.urls import reverse

from .views import REGISTRATION_SESSION_KEY


class StudentRegistrationWorkflowTests(TestCase):
    def setUp(self):
        self.valid_registration = {
            "student_name": "Asha Rao",
            "college_name": "Osmania University",
            "mobile_number": "9876543210",
            "passed_out_year": "2025",
        }

    def test_public_pages_render(self):
        for route_name in (
            "home",
            "about_ceo",
            "about_institute",
            "contact",
            "student_registration",
        ):
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_registration_saves_details_and_redirects_to_courses(self):
        response = self.client.post(
            reverse("student_registration"),
            self.valid_registration,
        )

        self.assertRedirects(response, reverse("courses"))
        self.assertEqual(
            self.client.session[REGISTRATION_SESSION_KEY]["student_name"],
            "Asha Rao",
        )
        self.assertEqual(
            self.client.session[REGISTRATION_SESSION_KEY]["college_name"],
            "Osmania University",
        )
        self.assertEqual(
            self.client.session[REGISTRATION_SESSION_KEY]["mobile_number"],
            "9876543210",
        )
        self.assertEqual(
            self.client.session[REGISTRATION_SESSION_KEY]["passed_out_year"],
            2025,
        )
        self.assertEqual(self.client.get(reverse("courses")).status_code, 200)

    def test_invalid_mobile_number_is_rejected(self):
        for mobile_number in ("12345", "abcdefghij"):
            with self.subTest(mobile_number=mobile_number):
                invalid_registration = {
                    **self.valid_registration,
                    "mobile_number": mobile_number,
                }
                response = self.client.post(
                    reverse("student_registration"),
                    invalid_registration,
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Enter exactly 10 digits.")
                self.assertNotIn(REGISTRATION_SESSION_KEY, self.client.session)

    def test_invalid_name_and_future_year_are_rejected(self):
        invalid_registration = {
            **self.valid_registration,
            "student_name": "Asha_123",
            "passed_out_year": str(date.today().year + 1),
        }

        response = self.client.post(
            reverse("student_registration"),
            invalid_registration,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid name")
        self.assertContains(response, "Passed out year cannot be in the future.")

    def test_courses_require_registration(self):
        response = self.client.get(reverse("courses"))

        self.assertRedirects(response, reverse("student_registration"))

    def test_courses_show_program_curricula_and_registration_options(self):
        self.client.post(
            reverse("student_registration"),
            self.valid_registration,
        )

        response = self.client.get(reverse("courses"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Java Full Stack Development with AI Integration and AWS Cloud",
        )
        self.assertContains(
            response,
            "Python Full Stack Development with AI/ML and AWS",
        )
        self.assertContains(response, "Spring Boot and dependency injection")
        self.assertContains(response, "Django REST Framework")
        self.assertContains(response, "View all 48 topics")
        self.assertContains(response, "View all 37 topics")
        self.assertContains(response, "Aptitude training")
        self.assertEqual(response.content.count(b"Select this course"), 2)
        self.assertNotContains(response, "AI Integration</h3>")
        self.assertNotContains(response, "AWS Cloud</h3>")
        self.assertNotContains(response, "Available batch")
        self.assertNotContains(response, "October 2026")
        self.assertNotContains(response, "Nov 2026")
        self.assertNotContains(response, "forms.gle")
        self.assertNotContains(response, "View registration options")

    def test_course_interest_encodes_message_and_clears_session(self):
        self.client.post(
            reverse("student_registration"),
            self.valid_registration,
        )

        response = self.client.get(
            reverse(
                "course_interest",
                kwargs={"course_slug": "python-full-stack"},
            )
        )

        self.assertEqual(response.status_code, 302)
        url = urlsplit(response.headers["Location"])
        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.netloc, "wa.me")
        self.assertEqual(url.path, "/918977149444")
        message = parse_qs(url.query)["text"][0]
        self.assertIn("Name: Asha Rao", message)
        self.assertIn("College Name: Osmania University", message)
        self.assertIn("Mobile Number: 9876543210", message)
        self.assertIn("Passed Out Year: 2025", message)
        self.assertIn("Interested Course: Python Full Stack", message)
        self.assertNotIn(REGISTRATION_SESSION_KEY, self.client.session)
