from urllib.parse import quote

from django.shortcuts import redirect, render

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

WHATSAPP_NUMBER = "918977149444"
REGISTRATION_SESSION_KEY = "student_registration"


def home(request):
    return render(request, "home.html")


def student_registration(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            request.session[REGISTRATION_SESSION_KEY] = form.cleaned_data
            return redirect("courses")
    else:
        form = StudentRegistrationForm()

    return render(request, "student.html", {"form": form})


def courses(request):
    if not request.session.get(REGISTRATION_SESSION_KEY):
        return redirect("student_registration")
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


def course_interest(request, course_slug):
    registration = request.session.get(REGISTRATION_SESSION_KEY)
    if not registration:
        return redirect("student_registration")

    course = next(
        (item for item in COURSES if item["slug"] == course_slug),
        None,
    )
    if course is None:
        return redirect("courses")

    message = (
        "Hello VTalent Institute,\n\n"
        "I am interested in joining your institute.\n\n"
        "Student Details:\n"
        f"Name: {registration['student_name']}\n"
        f"College Name: {registration['college_name']}\n"
        f"Mobile Number: {registration['mobile_number']}\n"
        f"Passed Out Year: {registration['passed_out_year']}\n\n"
        f"Interested Course: {course['name']}\n\n"
        "Please share the course details, fees, batch timings and admission information.\n\n"
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
