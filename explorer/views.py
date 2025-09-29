from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import CSVUploadForm, ImageUploadForm
from .utils import process_csv, process_image, generate_report
from .report_view import download_report

# Import plotting utilities
try:
    from .plotting_utils import generate_anomaly_plots, generate_image_plots
    PLOTTING_AVAILABLE = True
except ImportError as e:
    PLOTTING_AVAILABLE = False
    print(f"Plotting utilities not available: {e}")

# Create your views here.

def dashboard(request):
    csv_form = CSVUploadForm()
    image_form = ImageUploadForm()
    
    # Get results from session if available
    image_results = request.session.get('image_results', None)
    uploaded_file_path = request.session.get('uploaded_file_path', None)
    csv_results = request.session.get('csv_results', None)
    
    # Generate plots if results are available
    csv_plots = {}
    image_plots = {}
    
    if csv_results and PLOTTING_AVAILABLE:
        try:
            csv_plots = generate_anomaly_plots(csv_results)
        except Exception as e:
            print(f"Error generating CSV plots: {e}")
    
    if image_results and PLOTTING_AVAILABLE:
        try:
            image_plots = generate_image_plots(image_results)
        except Exception as e:
            print(f"Error generating image plots: {e}")
    
    context = {
        'csv_form': csv_form,
        'image_form': image_form,
        'image_results': image_results,
        'uploaded_file_path': uploaded_file_path,
        'csv_results': csv_results,
        'csv_plots': csv_plots,
        'image_plots': image_plots,
    }
    return render(request, 'dashboard.html', context)


def upload_csv(request):
    """
    Handle CSV file upload and processing with ML models.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            
            try:
                # Process the CSV file using ML models
                results = process_csv(csv_file)
                
                # Store results in session for dashboard display
                request.session['csv_results'] = results
                
                # Add success message
                messages.success(request, f'CSV file "{csv_file.name}" processed successfully with ML models!')
                
                # Redirect to dashboard with CSV results tab
                return redirect('dashboard')
                
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
    Handle image file upload and processing for mineral anomaly detection.
    """
    import os
    from django.conf import settings
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image_file']
            
            try:
                # Save the uploaded file to MEDIA_ROOT
                file_path = default_storage.save(f"uploads/{image_file.name}", ContentFile(image_file.read()))
                
                # Log the upload start
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"🚀 Starting image processing for: {image_file.name} (size: {image_file.size} bytes)")
                
                # Process the image file using our mock ML function
                results = process_image(image_file)
                
                logger.info(f"✅ Image processing completed for: {image_file.name}")
                logger.info(f"📊 Results: {results.get('status')} - {len(results.get('anomaly_zones', []))} zones detected")
                
                # Store results in session for dashboard display
                request.session['image_results'] = results
                request.session['uploaded_file_path'] = file_path
                
                # Add success message
                messages.success(request, f'Image file "{image_file.name}" processed successfully!')
                
                # Redirect to dashboard with image results tab active
                return redirect('dashboard')
                
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"❌ Error processing image file {image_file.name}: {str(e)}")
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


def download_image_report(request):
    """
    Generate and download PDF report for image analysis results.
    """
    if request.method == 'POST':
        # Get image results from session
        image_results = request.session.get('image_results', None)
        
        if not image_results:
            messages.error(request, 'No image analysis results found. Please upload and analyze an image first.')
            return redirect('dashboard')
        
        try:
            # Generate PDF report using the results
            response = generate_report(image_results, report_type='image')
            return response
            
        except Exception as e:
            messages.error(request, f'Error generating report: {str(e)}')
            return redirect('dashboard')
    
    return redirect('dashboard')