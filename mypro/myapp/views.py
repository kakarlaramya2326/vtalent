from pathlib import Path
from urllib.parse import quote

from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import StudentRegistrationForm


COURSES = [
    {
        "slug": "python-full-stack",
        "number": "02",
        "category": "FULL STACK DEVELOPMENT",
        "name": "Python Full Stack Development with AI/ML and AWS",
        "short_name": "Python Full Stack",
        "description": "Learn Python programming, front-end development, databases, Django web development, REST APIs, AI/ML fundamentals, and AWS Cloud. Build real-time projects and prepare for technical interviews with placement assistance.",
        "duration": "6 months",
        "background_image": "Registerpage/python-training-leadpro.webp",
        "topic_count": 37,
        "icon": "bi-code-slash",
        "modules": [
            {
                "name": "Core Python",
                "topics": [
                    "Python basics, variables, data types and operators",
                    "Conditional statements, loops and pattern programs",
                    "Strings, lists, tuples, sets and dictionaries",
                    "Functions, recursion, OOP, exceptions and file handling",
                ],
            },
            {
                "name": "Front-End Development",
                "topics": [
                    "HTML5 and CSS3",
                    "JavaScript fundamentals and DOM",
                    "Bootstrap and responsive web design",
                ],
            },
            {
                "name": "Database Management",
                "topics": [
                    "SQL fundamentals and MySQL",
                    "CRUD operations, joins, grouping and subqueries",
                    "Database integration with Python",
                ],
            },
            {
                "name": "Django Back-End Development",
                "topics": [
                    "Django project and app structure",
                    "Models, views, templates and URL routing",
                    "Forms, authentication and CRUD applications",
                    "Django ORM and database integration",
                ],
            },
            {
                "name": "Advanced Development",
                "topics": [
                    "REST API fundamentals",
                    "Django REST Framework",
                    "Git and GitHub",
                    "Testing, debugging and application security basics",
                ],
            },
            {
                "name": "AI/ML Fundamentals",
                "topics": [
                    "NumPy, Pandas and data visualization",
                    "Machine learning fundamentals",
                    "Model training and evaluation",
                    "Integrating ML models into web applications",
                ],
            },
            {
                "name": "AWS Cloud",
                "topics": [
                    "Cloud computing fundamentals",
                    "AWS core services and deployment concepts",
                    "Deploying a web application to the cloud",
                ],
            },
            {
                "name": "Real-Time Projects and Career Preparation",
                "topics": [
                    "Full-stack web application",
                    "Database integration and deployment",
                    "Resume preparation, mock interviews and placement assistance",
                ],
            },
        ],
    },
    {
        "slug": "java-full-stack",
        "number": "01",
        "category": "FULL STACK DEVELOPMENT",
        "name": "Java Full Stack Development with AI Integration and AWS Cloud",
        "short_name": "Java Full Stack",
        "description": "Learn Java programming from fundamentals to advanced concepts, front-end development, database management, back-end application development using Spring Boot, REST APIs, AI integration, and AWS Cloud deployment. Build real-time projects and prepare for technical interviews with placement assistance.",
        "duration": "6 months",
        "background_image": "Registerpage/java-training-institute.webp",
        "topic_count": 48,
        "icon": "bi-braces",
        "modules": [
            {
                "name": "Core Java",
                "topics": [
                    "Introduction to Java, JDK, JRE and JVM",
                    "Variables, data types, operators and control statements",
                    "Loops, arrays and strings",
                    "Classes, objects, constructors and methods",
                    "Inheritance, polymorphism, abstraction and encapsulation",
                    "Exception handling and packages",
                ],
            },
            {
                "name": "Advanced Java",
                "topics": [
                    "Collections Framework and Generics",
                    "Multithreading and file handling",
                    "Lambda expressions and Stream API",
                    "JDBC and database connectivity",
                    "Servlets and JSP fundamentals",
                ],
            },
            {
                "name": "Front-End Development",
                "topics": [
                    "HTML5 and CSS3",
                    "JavaScript fundamentals and DOM",
                    "Bootstrap and responsive web design",
                    "React fundamentals",
                ],
            },
            {
                "name": "Database Management",
                "topics": [
                    "SQL and MySQL",
                    "Tables, constraints and relationships",
                    "CRUD operations, joins and subqueries",
                    "Database integration with Java",
                ],
            },
            {
                "name": "Back-End Development",
                "topics": [
                    "Spring Framework fundamentals",
                    "Spring Boot and dependency injection",
                    "REST API development",
                    "Spring MVC and Spring Data JPA",
                    "Hibernate ORM",
                    "Validation, exception handling and authentication basics",
                ],
            },
            {
                "name": "AI Integration",
                "topics": [
                    "Introduction to AI and generative AI",
                    "Working with AI APIs",
                    "Integrating AI services into Java applications",
                    "Building an AI-powered application",
                ],
            },
            {
                "name": "AWS Cloud",
                "topics": [
                    "Cloud computing fundamentals",
                    "AWS IAM, EC2 and S3 fundamentals",
                    "Application deployment concepts",
                    "Environment configuration and cloud security basics",
                ],
            },
            {
                "name": "Real-Time Projects and Career Preparation",
                "topics": [
                    "Full-stack web application using Java and Spring Boot",
                    "Front-end and database integration",
                    "AI-integrated application",
                    "Git and GitHub",
                    "Testing, debugging and deployment",
                    "Resume preparation, coding practice and mock interviews",
                ],
            },
        ],
    },
]

INTERNSHIPS = [
    {
        "slug": "python-internship-45-days",
        "name": "Python Development Internship",
        "short_name": "Python Internship",
        "duration": "45 days",
        "background_image": "Registerpage/python-training-leadpro.webp",
        "icon": "bi-filetype-py",
        "description": "Learn core Python subjects through guided coding practice and a hands-on project.",
        "topics": [
            "Python syntax, variables, data types, and operators",
            "Conditional statements, loops, and problem solving",
            "Strings, lists, tuples, sets, and dictionaries",
            "Functions and object-oriented programming",
            "Exceptions and file handling",
            "Guided project development and presentation",
        ],
    },
    {
        "slug": "java-internship-45-days",
        "name": "Java Development Internship",
        "short_name": "Java Internship",
        "duration": "45 days",
        "background_image": "Registerpage/java-training-institute.webp",
        "icon": "bi-cup-hot",
        "description": "Learn core Java subjects through guided coding practice and a hands-on project.",
        "topics": [
            "Java syntax, variables, data types, and operators",
            "Conditional statements, loops, and problem solving",
            "Arrays, strings, and methods",
            "Classes, objects, and object-oriented programming",
            "Collections and exception handling",
            "Guided project development and presentation",
        ],
    },
    {
        "slug": "sql-internship-45-days",
        "name": "SQL Database Internship",
        "short_name": "SQL Internship",
        "duration": "45 days",
        "background_image": "",
        "icon": "bi-database",
        "description": "Learn core relational database concepts and SQL through query practice and a guided project.",
        "topics": [
            "Tables, data types, and database relationships",
            "SELECT queries, filtering, sorting, and functions",
            "INSERT, UPDATE, DELETE, and data integrity",
            "Joins, grouping, and subqueries",
            "Database design and normalization basics",
            "Guided database project and presentation",
        ],
    },
    {
        "slug": "ai-ml-internship-45-days",
        "name": "AI & Machine Learning Internship",
        "short_name": "AI/ML Internship",
        "duration": "45 days",
        "background_image": "Registerpage/ai_ml background.jpg",
        "icon": "bi-robot",
        "description": "Explore AI and machine learning foundations with practical data exercises and a guided beginner project.",
        "topics": [
            "AI and machine learning foundations",
            "Python tools for working with data",
            "Data cleaning and exploratory analysis",
            "Introduction to supervised learning",
            "Training, testing, and evaluating a simple model",
            "Guided beginner project and presentation",
        ],
    },
    {
        "slug": "aws-internship-45-days",
        "name": "AWS Cloud Internship",
        "short_name": "AWS Internship",
        "duration": "45 days",
        "background_image": "Registerpage/aws background.jpg",
        "icon": "bi-cloud",
        "description": "Learn cloud computing and AWS foundations through guided labs and a simple deployment project.",
        "topics": [
            "Cloud computing and AWS fundamentals",
            "AWS account, regions, and availability zones",
            "IAM users, roles, and basic access management",
            "Core services including EC2 and S3",
            "Basic networking, security, and cost awareness",
            "Deploying a simple project and presenting the result",
        ],
    },
]

# Add confirmed student stories here only after getting permission to publish them.
# Student photos should use paths under static/, e.g. images/students/name.jpg.
PLACEMENT_STUDENTS = []
# Company entries use {"name": "...", "logo": "images/companies/name.png"}; logo is optional.
PLACEMENT_COMPANIES = []
# Reel entries use {"title": "...", "url": "...", "thumbnail": "images/..."}.
INSTAGRAM_REELS = [
    {
        "title": "New Batch Starting December 2nd",
        "url": "https://www.instagram.com/reel/DfmBX_gRmRG/",
        "thumbnail": "images/instagram-reels/DfmBX_gRmRG.jpg",
    },
    {
        "title": "Congratulations to Our Students",
        "url": "https://www.instagram.com/reel/DeUBkeypw4z/",
        "thumbnail": "images/instagram-reels/DeUBkeypw4z.jpg",
    },
    {
        "title": "New Batch Starting October 28",
        "url": "https://www.instagram.com/reel/DeMvYd-pRwP/",
        "thumbnail": "images/instagram-reels/DeMvYd-pRwP.jpg",
    },
]
# Interview entries use {"title": "...", "video_id": "YouTube video ID"}.
YOUTUBE_INTERVIEWS = [
    {
        "title": "Before Joining Any IT Institute, Watch This!",
        "channel": "Vtalent Hyd",
        "video_id": "ObGBTAsR2E0",
    },
    {
        "title": "Best Career Advice in IT Industry You’ll Ever Get!",
        "channel": "Vtalent IT Academy",
        "video_id": "OxSGJ3HYm1Q",
    },
]

WHATSAPP_NUMBER = "918977149444"
REGISTRATION_SESSION_KEY = "student_registration"
PLACEMENT_PHOTO_DIRECTORY = (
    Path(__file__).resolve().parent.parent / "static" / "pplacement pics"
)


def get_placement_photos():
    supported_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    if not PLACEMENT_PHOTO_DIRECTORY.is_dir():
        return []

    return [
        f"pplacement pics/{photo.name}"
        for photo in sorted(
            PLACEMENT_PHOTO_DIRECTORY.iterdir(),
            key=lambda photo: photo.stem.casefold(),
        )
        if photo.is_file() and photo.suffix.lower() in supported_extensions
    ]


def home(request):
    placement_photos = get_placement_photos()
    return render(
        request,
        "home.html",
        {
            "courses": COURSES,
            "internships": INTERNSHIPS,
            "full_stack_courses": sorted(
                COURSES,
                key=lambda course: course["number"],
            ),
            "placement_students": PLACEMENT_STUDENTS,
            "placement_photos": placement_photos,
            "placement_photo_groups": (placement_photos, placement_photos),
            "placement_companies": PLACEMENT_COMPANIES,
            "instagram_reels": INSTAGRAM_REELS,
            "youtube_interviews": YOUTUBE_INTERVIEWS,
        },
    )


def student_registration(request):
    selected_course_slug = request.POST.get("course") or request.GET.get("course")
    selected_course = next(
        (
            item
            for item in COURSES
            if item["slug"] == selected_course_slug
        ),
        None,
    )
    selected_internship = next(
        (
            item
            for item in INTERNSHIPS
            if item["slug"] == selected_course_slug
        ),
        None,
    )

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.cleaned_data
            request.session[REGISTRATION_SESSION_KEY] = registration
            if registration["program_type"] == "internship":
                if selected_internship is not None:
                    return redirect(
                        "course_interest",
                        course_slug=selected_internship["slug"],
                    )
                return redirect("internships")
            if selected_course is not None:
                return redirect(
                    "course_interest",
                    course_slug=selected_course["slug"],
                )
            return redirect("courses")
    else:
        initial = {}
        requested_program_type = request.GET.get("program_type")
        if requested_program_type in {"internship", "coaching"}:
            initial["program_type"] = requested_program_type
        elif selected_course is not None:
            initial["program_type"] = "coaching"
        elif selected_internship is not None:
            initial["program_type"] = "internship"
        form = StudentRegistrationForm(initial=initial)

    return render(
        request,
        "student.html",
        {
            "form": form,
            "selected_course": selected_course,
            "selected_internship": selected_internship,
            "selected_course_slug": selected_course_slug,
            "internships": INTERNSHIPS,
        },
    )


def courses(request):
    return render(
        request,
        "course.html",
        {
            "full_stack_courses": sorted(
                COURSES,
                key=lambda course: course["number"],
            ),
        },
    )


def internships(request):
    return render(request, "intenships.html", {"internships": INTERNSHIPS})


def student_placements(request):
    placement_photos = get_placement_photos()
    return render(
        request,
        "placesstudent.html",
        {
            "placement_students": PLACEMENT_STUDENTS,
            "placement_photos": placement_photos,
            "placement_photo_groups": (placement_photos, placement_photos),
            "placement_companies": PLACEMENT_COMPANIES,
        },
    )


def course_interest(request, course_slug):
    registration = request.session.get(REGISTRATION_SESSION_KEY)
    if not registration:
        if any(item["slug"] == course_slug for item in INTERNSHIPS):
            return redirect(
                f"{reverse('student_registration')}?program_type=internship"
            )
        return redirect("student_registration")

    course = next(
        (item for item in COURSES if item["slug"] == course_slug),
        None,
    )
    internship = next(
        (item for item in INTERNSHIPS if item["slug"] == course_slug),
        None,
    )
    program_type = registration.get("program_type", "coaching")
    if internship is not None:
        if program_type != "internship":
            return redirect("courses")
        selected_program = internship
        program_label = "Internship"
    elif course is not None:
        if program_type != "coaching":
            return redirect("internships")
        selected_program = course
        program_label = "Six-month coaching course"
    else:
        return redirect("internships" if program_type == "internship" else "courses")

    message = (
        "Hello VTalent Institute,\n\n"
        "I am interested in joining your institute.\n\n"
        "Student Details:\n"
        f"Name: {registration['student_name']}\n"
        f"College Name: {registration['college_name']}\n"
        f"Mobile Number: {registration['mobile_number']}\n"
        f"Passed Out Year: {registration['passed_out_year']}\n\n"
        f"Interested Program: {selected_program['name']}\n"
        f"Program Type: {program_label}\n"
        f"Duration: {selected_program['duration']}\n\n"
        "Please share the program details, fees, batch timings and admission information.\n\n"
        "Thank you."
    )
    whatsapp_url = (
        f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message, safe='')}"
    )
    request.session.pop(REGISTRATION_SESSION_KEY, None)
    return redirect(whatsapp_url)


def about_ceo(request):
    return render(request, "aboutceo.html")


def about_institute(request):
    return render(request, "aboutinstitute.html")


def contact(request):
    return render(request, "contact.html")
