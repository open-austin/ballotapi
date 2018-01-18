from django.urls import path
from django.views.generic import TemplateView

app_name = "static_pages"

urlpatterns = [

    # landing
    path('', TemplateView.as_view(template_name='landing.html', extra_context={
        "title": "Home",
        "nav": "home",
    }), name='landing'),

    # about
    path('about/', TemplateView.as_view(template_name='about.html', extra_context={
        "title": "About",
        "nav": "about",
    }), name='about'),
]
