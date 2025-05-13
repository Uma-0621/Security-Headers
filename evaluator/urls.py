from django.urls import path
from . import views
from .views import evaluate_headers, ReactAppView

urlpatterns = [
    path('api/evaluate/', evaluate_headers, name='evaluate_headers'),  # API endpoint
    path('', ReactAppView.as_view(), name='react_app'),                # Catch-all route to serve React index.html
]


