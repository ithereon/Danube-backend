from django.urls import path
from . import views

urlpatterns = [
    path("dealing-with-mould", views.blog1, name="blogs"),
    path(
        "Plumbing-dos-and-donts-for-home-and-property-owners/Hire-a-plumber/10-essential-tips-to-choosing-a-plumber",
        views.blog2,
        name="blog2",
    ),
    path(
        "Hire-a-builder/How-to-find-a-builder/14-essential-tips-to-help-homeowners-and-builders-with-projects",
        views.blog3,
        name="blog3",
    ),
    path(
        "Electrical-safety-dos-and-donts-for-homeowners/How-to-find-a-reliable-Electrician/Electricians-and-Solar",
        views.blog4,
        name="blog4",
    ),
    path(
        "Hire-a-builder/How-to-find-a-builder/dealing-with-asbestos",
        views.blog5,
        name="blog5",
    ),
    path("12-step-essential-guide-home-and-cold-weather", views.blog6, name="blog6"),
    path("10-step-guide-to-kitchen-renovation-project", views.blog7, name="blog7"),
    path("18-point-guide-to-organising-a-home-move", views.blog8, name="blog8"),
    path(
        "Why-apprentices-are-important-for-the-future-of-the-trade",
        views.blog9,
        name="blog9",
    ),
    path(
        "17-essential-tips-to-help-you-with-hydroponic-gardening",
        views.blog10,
        name="blog10",
    ),
    path("6-points-to-consider-in-a-garange-conversion", views.blog11, name="blog11"),
    path(
        "13-steps-to-declutter-a-storage-room-and-make-money",
        views.blog12,
        name="blog12",
    ),
    path(
        "12-quick-tips-to-reduce-the-risk-of-a-burglary-at-your-home",
        views.blog13,
        name="blog13",
    ),
    path("Hire-a-builder/How-to-find-a-builder", views.blog14, name="blog14"),
    path("Hire-a-builder", views.blog15, name="blog15"),
    path(
        "Plumbing-dos-and-donts-for-home-and-property-owners/Hire-a-plumber",
        views.blog16,
        name="blog16",
    ),
    path("Electrical-safety-dos-and-donts-for-homeowners", views.blog17, name="blog17"),
    path(
        "Electrical-safety-dos-and-donts-for-homeowners/How-to-find-a-reliable-Electrician",
        views.blog18,
        name="blog18",
    ),
    path(
        "Plumbing-dos-and-donts-for-home-and-property-owners",
        views.blog19,
        name="blog19",
    ),
    path(
        "Everything-you-need-to-know-about-hiring-a-painter",
        views.blog20,
        name="blog20",
    ),
]
