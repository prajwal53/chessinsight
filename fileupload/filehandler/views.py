
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
from wsgiref.util import FileWrapper
from django.shortcuts import get_object_or_404
import mimetypes
import os
from django.http import HttpResponseBadRequest


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            print("File Saved Successfully:", uploaded_file.file.name)
            return redirect('upload_success')
        else:
            print("Form is not valid:", form.errors)
            return HttpResponseBadRequest("Form submission failed. Please check the form errors.")
    else:
        form = UploadFileForm()
    return render(request, 'filehandler/upload.html', {'form': form})

def download_file(request):
    latest_file = UploadedFile.objects.last()
    print("Latest File:", latest_file)
    return render(request, 'filehandler/download.html', {'latest_file': latest_file})


def download_pdf(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    with open(uploaded_file.file.path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response

def upload_success(request):
    return render(request, 'filehandler/upload_success.html')