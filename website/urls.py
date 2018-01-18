from django.urls import include, path

urlpatterns = [
    path('docs/', include('docs.urls')),
    path('', include('static_pages.urls')),
]
