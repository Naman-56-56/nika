from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import CSVUploadForm, ImageUploadForm
from .utils import process_csv, process_image, generate_report
from .report_view import download_report

# Create your views here.

def dashboard(request):
    csv_form = CSVUploadForm()
    image_form = ImageUploadForm()
    
    context = {
        'csv_form': csv_form,
        'image_form': image_form,
    }
    return render(request, 'dashboard.html', context)


def upload_csv(request):
    """
    Handle CSV file upload and processing.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            
            try:
                # Process the CSV file using our mock function
                results = process_csv(csv_file)
                
                # Add success message
                messages.success(request, f'CSV file "{csv_file.name}" processed successfully!')
                
                # Render results template with processed data
                context = {
                    'results': results,
                    'file_type': 'csv'
                }
                return render(request, 'csv_results.html', context)
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                return redirect('dashboard')
        else:
            # Form is not valid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('dashboard')


def upload_image(request):
    """
    Handle image file upload and processing.
    """
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image_file']
            
            try:
                # Process the image file using our mock function
                results = process_image(image_file)
                
                # Add success message
                messages.success(request, f'Image file "{image_file.name}" processed successfully!')
                
                # Render results template with processed data
                context = {
                    'results': results,
                    'file_type': 'image'
                }
                return render(request, 'image_results.html', context)
                
            except Exception as e:
                messages.error(request, f'Error processing image file: {str(e)}')
                return redirect('dashboard')
        else:
            # Form is not valid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('dashboard')
    
    # If GET request, redirect to dashboard
    return redirect('dashboard')
