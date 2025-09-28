def download_report(request):
    """
    Generate and download a PDF report based on session data or mock data.
    """
    from django.shortcuts import redirect
    from django.contrib import messages
    from .utils import generate_report
    
    # For demo purposes, we'll generate a mock report
    # In a real application, you would retrieve actual results from session/database
    
    report_type = request.GET.get('type', 'csv')
    
    if report_type == 'csv':
        # Generate mock CSV results for demo
        mock_results = {
            'status': 'success',
            'file_info': {
                'filename': 'sample_data.csv',
                'size_bytes': 2048000,
                'processed_at': '2025-09-28 14:30:00'
            },
            'metrics': {
                'total_records': 5000,
                'anomalies_detected': 12,
                'processing_time': 3.2,
                'baseline_metrics': {
                    'f1_score': 0.600,
                    'precision': 0.580,
                    'recall': 0.620,
                    'accuracy': 0.820
                },
                'nika_metrics': {
                    'f1_score': 0.780,
                    'precision': 0.785,
                    'recall': 0.775,
                    'accuracy': 0.920
                },
                'improvement_percentage': {
                    'f1_score': 30.0,
                    'precision': 18.5,
                    'recall': 15.2,
                    'accuracy': 12.8
                }
            },
            'anomalies': [
                {
                    'id': 'anomaly_1',
                    'type': 'Statistical Outlier',
                    'severity': 'Critical',
                    'confidence': 0.945,
                    'timestamp': '2025-09-28 10:15:23'
                },
                {
                    'id': 'anomaly_2',
                    'type': 'Temporal Pattern Deviation',
                    'severity': 'High',
                    'confidence': 0.887,
                    'timestamp': '2025-09-28 11:22:15'
                }
            ]
        }
    else:
        # Generate mock image results for demo
        mock_results = {
            'status': 'success',
            'file_info': {
                'filename': 'inspection_image.jpg',
                'format': 'JPG',
                'size_bytes': 1024000,
                'processed_at': '2025-09-28 14:30:00'
            },
            'analysis_results': {
                'total_patches': 5,
                'high_confidence_patches': 3,
                'critical_anomalies': 2,
                'processing_time': 8.7,
                'detection_metrics': {
                    'sensitivity': 0.892,
                    'specificity': 0.934,
                    'precision': 0.856
                },
                'image_quality': {
                    'clarity_score': 0.891,
                    'contrast_score': 0.823
                }
            },
            'patches': [
                {
                    'id': 'patch_1',
                    'type': 'Surface Crack',
                    'severity': 'Critical',
                    'confidence': 0.945,
                    'center_coordinates': {'x': 234, 'y': 567}
                },
                {
                    'id': 'patch_2',
                    'type': 'Corrosion Spot',
                    'severity': 'High',
                    'confidence': 0.887,
                    'center_coordinates': {'x': 456, 'y': 123}
                }
            ],
            'recommendations': [
                "⚠️ Immediate attention required for critical anomalies detected",
                "🔧 Schedule emergency maintenance for affected areas",
                "📋 Plan detailed inspection of high-severity anomalies"
            ]
        }
    
    # Generate and return PDF report
    try:
        return generate_report(mock_results, report_type)
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('dashboard')