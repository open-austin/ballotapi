from django.urls import path
from django.views.generic import TemplateView

app_name = "docs"

urlpatterns = [

    # informational pages
    path('', TemplateView.as_view(template_name='docs/info_overview.html', extra_context={
        "title": "Documentation",
        "nav": "docs",
        "toc": "overview",
    }), name='overview'),
    path('quickstart', TemplateView.as_view(template_name='docs/info_quickstart.html', extra_context={
        "title": "Quickstart",
        "nav": "docs",
        "toc": "quickstart",
    }), name='quickstart'),
    path('examples', TemplateView.as_view(template_name='docs/info_examples.html', extra_context={
        "title": "Examples",
        "nav": "docs",
        "toc": "examples",
    }), name='examples'),
    path('data-types', TemplateView.as_view(template_name='docs/info_data_types.html', extra_context={
        "title": "Data Types",
        "nav": "docs",
        "toc": "data_types",
    }), name='data_types'),
    path('testing', TemplateView.as_view(template_name='docs/info_testing.html', extra_context={
        "title": "Testing",
        "nav": "docs",
        "toc": "testing",
    }), name='testing'),
    path('rate-limits', TemplateView.as_view(template_name='docs/info_rate_limits.html', extra_context={
        "title": "Rate Limits",
        "nav": "docs",
        "toc": "rate_limits",
    }), name='rate_limits'),
    path('api', TemplateView.as_view(template_name='docs/api_endpoints.html', extra_context={
        "title": "API Endpoints",
        "nav": "docs",
        "toc": "api_endpoints",
    }), name='api_endpoints'),

    # Elections
    path('api/elections', TemplateView.as_view(template_name='docs/api_elections_object.html', extra_context={
        "title": "Elections",
        "nav": "docs",
        "toc": "api_elections",
        "subtoc": "api_elections_object",
    }), name='api_elections_object'),
    path('api/elections/list', TemplateView.as_view(template_name='docs/api_elections_list.html', extra_context={
        "title": "Elections - List",
        "nav": "docs",
        "toc": "api_elections",
        "subtoc": "api_elections_list",
    }), name='api_elections_list'),
    path('api/elections/get', TemplateView.as_view(template_name='docs/api_elections_get.html', extra_context={
        "title": "Elections - Get",
        "nav": "docs",
        "toc": "api_elections",
        "subtoc": "api_elections_get",
    }), name='api_elections_get'),


    # Precincts
    path('api/precincts', TemplateView.as_view(template_name='docs/api_precincts_object.html', extra_context={
        "title": "Precincts",
        "nav": "docs",
        "toc": "api_precincts",
        "subtoc": "api_precincts_object",
    }), name='api_precincts_object'),
    path('api/precincts/list', TemplateView.as_view(template_name='docs/api_precincts_list.html', extra_context={
        "title": "Precincts - List",
        "nav": "docs",
        "toc": "api_precincts",
        "subtoc": "api_precincts_list",
    }), name='api_precincts_list'),
    path('api/precincts/get', TemplateView.as_view(template_name='docs/api_precincts_get.html', extra_context={
        "title": "Precincts - Get",
        "nav": "docs",
        "toc": "api_precincts",
        "subtoc": "api_precincts_get",
    }), name='api_precincts_get'),

    # Contests
    path('api/contests', TemplateView.as_view(template_name='docs/api_contests_object.html', extra_context={
        "title": "Contests",
        "nav": "docs",
        "toc": "api_contests",
        "subtoc": "api_contests_object",
    }), name='api_contests_object'),
    path('api/contests/list', TemplateView.as_view(template_name='docs/api_contests_list.html', extra_context={
        "title": "Contests - List",
        "nav": "docs",
        "toc": "api_contests",
        "subtoc": "api_contests_list",
    }), name='api_contests_list'),
    path('api/contests/get', TemplateView.as_view(template_name='docs/api_contests_get.html', extra_context={
        "title": "Contests - Get",
        "nav": "docs",
        "toc": "api_contests",
        "subtoc": "api_contests_get",
    }), name='api_contests_get'),
]
