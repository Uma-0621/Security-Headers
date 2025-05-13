from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import os
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Evaluation
from .serializers import EvaluationSerializer

# ------------------------------
# Serve React Frontend (index.html)
# ------------------------------
class ReactAppView(View):
    def get(self, request):
        try:
            file_path = os.path.join(settings.BASE_DIR, 'evaluator', 'frontend', 'index.html')
            with open(file_path, 'r') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse("React build not found. Please run npm run build.", status=501)

# ------------------------------
# Optional Home & Index Views
# ------------------------------
def home(request):
    return HttpResponse("Welcome to the Security Headers Evaluator!")

def index(request):
    return HttpResponse("Hello from Security Headers Evaluator App!")

# ------------------------------
# Security Headers to Check
# ------------------------------
SECURITY_HEADERS = {
    'Content-Security-Policy': 'CSP',
    'Strict-Transport-Security': 'HSTS',
    'X-Content-Type-Options': 'XCTO',
    'X-Frame-Options': 'XFO',
    'X-XSS-Protection': 'XXSSP',
    'Referrer-Policy': 'RP',
    'Permissions-Policy': 'PP',
}

# ------------------------------
# API Endpoint: Evaluate Headers
# ------------------------------
@api_view(['POST'])
def evaluate_headers(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = requests.get(url)
        headers = response.headers
    except requests.RequestException:
        return Response({'error': 'Failed to fetch the URL'}, status=status.HTTP_400_BAD_REQUEST)

    missing_headers = [header for header in SECURITY_HEADERS if header not in headers]

    # Determine grade
    if not missing_headers:
        grade = 'A+'
    elif len(missing_headers) <= 3:
        grade = 'B+'
    else:
        grade = 'C'

    # Generate PDF report
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Security Headers Evaluation Report for {url}")
    p.drawString(100, 730, f"Grade: {grade}")
    p.drawString(100, 710, "Missing Headers:")
    for i, header in enumerate(missing_headers, start=1):
        p.drawString(120, 710 - i * 20, header)
    p.showPage()
    p.save()
    buffer.seek(0)

    # Save Evaluation and Report
    evaluation = Evaluation.objects.create(url=url, grade=grade)
    evaluation.report.save(f'report_{evaluation.id}.pdf', buffer, save=True)

    return Response({
        'url': url,
        'grade': grade,
        'missing_headers': missing_headers,
        'report_url': evaluation.report.url
    })
