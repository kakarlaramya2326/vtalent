from datetime import date
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from django.contrib.staticfiles.storage import staticfiles_storage
from django.test import TestCase, override_settings
from django.urls import reverse

from .views import REGISTRATION_SESSION_KEY


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class StudentRegistrationWorkflowTests(TestCase):
    def setUp(self):
        self.valid_registration = {
            "program_type": "coaching",
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
            "student_placements",
            "internships",
        ):
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="reading-progress"')
                self.assertContains(response, 'class="back-to-top"')

    def test_homepage_shows_course_discovery_and_social_sections(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explore our programs")
        self.assertContains(response, 'class="institute-video"')
        self.assertContains(response, 'autoplay muted loop playsinline')
        self.assertContains(response, "vtalennanimation/vtalent(video).mp4")
        self.assertContains(response, 'id="highlights"')
        self.assertContains(response, "Training beyond")
        self.assertContains(response, "THE ONE AND ONLY INSTITUTION")
        self.assertContains(response, "A dedicated institute for eligible graduates")
        self.assertContains(response, "eligible CSE, IT, and ECE graduates only")
        self.assertContains(response, 'class="hero-highlights-track"')
        self.assertNotContains(response, "What makes VTalent different")
        self.assertNotContains(response, 'href="#highlights"')
        self.assertNotContains(response, ">Highlights</a>")
        self.assertContains(response, "45-day internships available")
        for track in ("Python", "Java", "SQL", "AI/ML"):
            with self.subTest(internship_track=track):
                self.assertEqual(
                    response.content.count(f"<strong>{track}</strong>".encode()),
                    2,
                )
        self.assertContains(response, 'class="hero-corporate-highlights"')
        self.assertContains(response, 'aria-labelledby="corporate-highlights-title"')
        self.assertContains(response, 'class="corporate-highlights-track"')
        self.assertContains(response, 'class="corporate-highlights-group" aria-hidden="true"')
        for highlight in (
            "Working professionals",
            "No partiality",
            "Placement support from onboarding",
            "Quality without compromise",
            "Current-year graduates",
        ):
            with self.subTest(corporate_highlight=highlight):
                self.assertEqual(response.content.count(highlight.encode()), 2)
        self.assertContains(response, "6-MONTH COACHING")
        self.assertContains(response, "Register for this course")
        self.assertContains(response, "VTalent Reels")
        self.assertContains(response, "Recent videos &amp; interviews")
        self.assertContains(
            response,
            "https://i.ytimg.com/vi/ObGBTAsR2E0/hqdefault.jpg",
        )
        self.assertContains(
            response,
            "https://i.ytimg.com/vi/OxSGJ3HYm1Q/hqdefault.jpg",
        )
        self.assertContains(response, "Watch on YouTube")
        self.assertNotContains(response, "<iframe")
        self.assertContains(
            response,
            "Before Joining Any IT Institute, Watch This!",
        )
        self.assertContains(
            response,
            "Best Career Advice in IT Industry You’ll Ever Get!",
        )
        self.assertNotContains(response, "Interviews coming soon")
        self.assertEqual(
            response.content.count(
                b"https://www.instagram.com/hyd.vtalent/?hl=en"
            ),
            1,
        )
        self.assertContains(response, "DfmBX_gRmRG.jpg")
        self.assertContains(response, "DeUBkeypw4z.jpg")
        self.assertContains(response, "DeMvYd-pRwP.jpg")
        self.assertContains(
            response,
            "Watch New Batch Starting December 2nd on Instagram",
        )
        self.assertContains(response, reverse("student_registration"))
        for section_id in (
            "home",
            "about-institute",
            "courses",
            "placements",
            "ceo",
            "community",
            "contact",
        ):
            with self.subTest(section=section_id):
                self.assertContains(response, f'id="{section_id}"')
        self.assertContains(response, 'href="#courses"')
        self.assertContains(response, 'href="#placements"')
        self.assertContains(response, "Prasad Mandava")
        self.assertContains(response, "A Vision to Empower Telugu Talent and Transform Careers")
        self.assertContains(response, "3,000+ students placed in the IT industry by 2024")
        self.assertContains(response, "represented across the global IT industry")
        self.assertContains(response, "Let’s start a conversation.")

    def test_home_programs_show_background_courses_and_scrollable_internships(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "home-course-card-python")
        self.assertContains(response, "home-course-card-java")
        self.assertContains(
            response,
            'role="region" aria-label="Scroll through 45-day internship programs"',
        )
        self.assertEqual(response.content.count(b'class="home-internship-card"'), 5)
        self.assertContains(response, "Register for this internship")
        course_backgrounds = {
            course["slug"]: course["background_image"]
            for course in response.context["courses"]
        }
        self.assertEqual(
            course_backgrounds["python-full-stack"],
            "Registerpage/Neon Python Code Horizon.png",
        )
        self.assertEqual(
            course_backgrounds["java-full-stack"],
            "Registerpage/java-training-institute.webp",
        )

    def test_internships_show_python_and_java_45_day_tracks(self):
        response = self.client.get(reverse("internships"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Development Internship")
        self.assertContains(response, "Java Development Internship")
        self.assertContains(response, "SQL Database Internship")
        self.assertContains(response, "AI &amp; Machine Learning Internship")
        self.assertContains(response, "AWS Cloud Internship")
        self.assertContains(response, "Core subjects you’ll learn")
        self.assertContains(response, "data types, and operators")
        self.assertContains(response, "object-oriented programming")
        self.assertEqual(
            [program["duration"] for program in response.context["internships"]],
            ["45 days"] * 5,
        )

    def test_student_placements_page_shows_uploaded_photos_without_invented_profiles(self):
        response = self.client.get(reverse("student_placements"))

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context["placement_photos"]), 0)
        self.assertEqual(
            response.context["placement_photos"],
            sorted(
                response.context["placement_photos"],
                key=lambda photo: photo.rsplit("/", 1)[-1].rsplit(".", 1)[0].casefold(),
            ),
        )
        self.assertContains(response, 'aria-label="VTalent student placement photos"')
        self.assertContains(response, 'class="placement-gallery-track"')
        self.assertContains(response, 'aria-hidden="true"')
        self.assertNotContains(response, "Student stories are coming soon")
        self.assertContains(response, "Company highlights will appear here")
        self.assertNotContains(response, "Amazon")

    @patch(
        "myapp.views.YOUTUBE_INTERVIEWS",
        [{"title": "Sample interview", "video_id": "abc123xyz00"}],
    )
    @patch(
        "myapp.views.INSTAGRAM_REELS",
        [
            {
                "title": "Sample reel",
                "url": "https://www.instagram.com/reel/sample/",
                "thumbnail": "images/instagram-reels/sample.jpg",
            }
        ],
    )
    @patch(
        "myapp.views.PLACEMENT_COMPANIES",
        [{"name": "Sample employer"}],
    )
    @patch(
        "myapp.views.PLACEMENT_STUDENTS",
        [
            {
                "name": "Sample learner",
                "course": "Python Full Stack",
                "company": "Sample employer",
                "role": "Developer",
                "quote": "A sample story.",
            }
        ],
    )
    def test_editable_home_and_placement_content_renders(self):
        home_response = self.client.get(reverse("home"))
        placements_response = self.client.get(reverse("student_placements"))

        self.assertContains(home_response, "Sample employer")
        self.assertContains(home_response, "Sample reel")
        self.assertContains(
            home_response,
            staticfiles_storage.url("images/instagram-reels/sample.jpg"),
        )
        self.assertContains(home_response, "Sample interview")
        self.assertContains(placements_response, "Sample learner")
        self.assertContains(placements_response, "Developer")

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

    def test_internship_registration_routes_to_internship_choices(self):
        response = self.client.post(
            reverse("student_registration"),
            {**self.valid_registration, "program_type": "internship"},
        )

        self.assertRedirects(response, reverse("internships"))
        self.assertEqual(
            self.client.session[REGISTRATION_SESSION_KEY]["program_type"],
            "internship",
        )

    def test_registration_shows_45_day_courses_with_backgrounds(self):
        response = self.client.get(
            reverse("student_registration"),
            {"program_type": "internship"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-program-type="internship"')
        self.assertContains(response, 'data-course-slug="java-internship-45-days"')
        self.assertContains(response, 'data-course-slug="python-internship-45-days"')
        self.assertContains(response, 'data-course-slug="ai-ml-internship-45-days"')
        self.assertContains(response, 'data-course-slug="aws-internship-45-days"')
        internship_backgrounds = {
            internship["slug"]: internship["background_image"]
            for internship in response.context["internships"]
        }
        self.assertEqual(
            internship_backgrounds["java-internship-45-days"],
            "Registerpage/java-training-institute.webp",
        )
        self.assertEqual(
            internship_backgrounds["python-internship-45-days"],
            "Registerpage/Neon Python Code Horizon.png",
        )
        python_image_url = staticfiles_storage.url(
            "Registerpage/Neon Python Code Horizon.png"
        )
        self.assertContains(
            response,
            f'src="{python_image_url}"',
        )
        self.assertEqual(
            internship_backgrounds["ai-ml-internship-45-days"],
            "Registerpage/ai_ml background.jpg",
        )
        self.assertEqual(
            internship_backgrounds["aws-internship-45-days"],
            "Registerpage/aws background.jpg",
        )

    def test_selected_internship_registration_routes_to_that_program(self):
        response = self.client.post(
            reverse("student_registration"),
            {
                **self.valid_registration,
                "program_type": "internship",
                "course": "aws-internship-45-days",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "course_interest",
                kwargs={"course_slug": "aws-internship-45-days"},
            ),
            fetch_redirect_response=False,
        )

    def test_internship_selection_prompts_for_internship_registration(self):
        response = self.client.get(
            reverse(
                "course_interest",
                kwargs={"course_slug": "java-internship-45-days"},
            )
        )

        self.assertRedirects(
            response,
            f"{reverse('student_registration')}?program_type=internship",
        )

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

    def test_invalid_name_is_rejected(self):
        invalid_registration = {
            **self.valid_registration,
            "student_name": "Asha_123",
        }

        response = self.client.post(
            reverse("student_registration"),
            invalid_registration,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid name")

    def test_future_passed_out_year_is_accepted(self):
        future_year = date.today().year + 1
        registration = {
            **self.valid_registration,
            "passed_out_year": str(future_year),
        }

        response = self.client.post(
            reverse("student_registration"),
            registration,
        )

        self.assertRedirects(response, reverse("courses"))
        self.assertEqual(
            self.client.session[REGISTRATION_SESSION_KEY]["passed_out_year"],
            future_year,
        )

    def test_courses_are_publicly_browsable(self):
        response = self.client.get(reverse("courses"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Java Full Stack Development")
        self.assertContains(response, "Python Full Stack Development")

    def test_course_selection_requires_registration(self):
        response = self.client.get(
            reverse(
                "course_interest",
                kwargs={"course_slug": "java-full-stack"},
            )
        )

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
        self.assertContains(response, "program-card-java")
        self.assertContains(response, "program-card-python")
        java_image_url = staticfiles_storage.url(
            "Registerpage/java-training-institute.webp"
        )
        python_image_url = staticfiles_storage.url(
            "Registerpage/Neon Python Code Horizon.png"
        )
        self.assertContains(
            response,
            f'class="program-card-background" src="{java_image_url}"',
        )
        self.assertContains(
            response,
            f'class="program-card-background" src="{python_image_url}"',
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
        self.assertIn("Interested Program: Python Full Stack", message)
        self.assertIn("Program Type: Six-month coaching course", message)
        self.assertNotIn(REGISTRATION_SESSION_KEY, self.client.session)

    def test_internship_interest_encodes_program_and_duration(self):
        self.client.post(
            reverse("student_registration"),
            {**self.valid_registration, "program_type": "internship"},
        )

        response = self.client.get(
            reverse(
                "course_interest",
                kwargs={"course_slug": "python-internship-45-days"},
            )
        )

        self.assertEqual(response.status_code, 302)
        message = parse_qs(urlsplit(response.headers["Location"]).query)["text"][0]
        self.assertIn("Interested Program: Python Development Internship", message)
        self.assertIn("Program Type: Internship", message)
        self.assertIn("Duration: 45 days", message)
        self.assertNotIn(REGISTRATION_SESSION_KEY, self.client.session)
