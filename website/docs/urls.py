from django.urls import path
from django.views.generic import TemplateView

app_name = "docs"

urlpatterns = [

    # informational pages
    path('', TemplateView.as_view(template_name='docs/overview.html', extra_context={
        "title": "Documentation",
        "nav": "docs",
        "toc": "overview",
    }), name='overview'),
]
