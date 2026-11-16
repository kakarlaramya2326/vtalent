"""
URL configuration for mypro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from myapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("student-registration/", views.student_registration, name="student_registration"),
    path("courses/", views.courses, name="courses"),
    path("student-placements/", views.student_placements, name="student_placements"),
    path(
        "courses/<slug:course_slug>/interest/",
        views.course_interest,
        name="course_interest",
    ),
    path("about/ceo/", views.about_ceo, name="about_ceo"),
    path("about/institute/", views.about_institute, name="about_institute"),
    path("contact/", views.contact, name="contact"),
]
