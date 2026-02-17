from django.http import HttpResponse
from datetime import datetime

def create_pdf_response(filename):
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def get_generated_date():
    return datetime.now().strftime("%d-%m-%Y %H:%M")
