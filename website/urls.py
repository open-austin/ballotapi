from django.urls import include, path

urlpatterns = [
    path('', include('static_pages.urls')),
]
