import random
import json
from datetime import datetime, timedelta
import io
from django.http import HttpResponse

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.platypus import Image as ReportLabImage
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics import renderPDF
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def process_csv(file):
    """
    Mock function to process CSV files and return fake anomalies and metrics.
    
    Args:
        file: Uploaded CSV file
        
    Returns:
        dict: Contains anomalies list and metrics dictionary
    """
    
    # Generate fake anomalies data
    anomalies = []
    num_anomalies = random.randint(3, 15)
    
    anomaly_types = [
        'Statistical Outlier',
        'Temporal Pattern Deviation',
        'Correlation Break',
        'Trend Anomaly',
        'Seasonal Deviation',
        'Value Range Violation',
        'Missing Data Pattern',
        'Frequency Anomaly'
    ]
    
    for i in range(num_anomalies):
        anomaly = {
            'id': f'anomaly_{i+1}',
            'type': random.choice(anomaly_types),
            'severity': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'confidence': round(random.uniform(0.65, 0.95), 3),
            'timestamp': (datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )).strftime('%Y-%m-%d %H:%M:%S'),
            'affected_columns': random.sample(['temperature', 'pressure', 'humidity', 'voltage', 'current', 'speed'], 
                                           random.randint(1, 3)),
            'description': f'Detected anomalous pattern in row {random.randint(1, 1000)}',
            'baseline_score': round(random.uniform(0.3, 0.7), 3),
            'nika_score': round(random.uniform(0.75, 0.95), 3)
        }
        anomalies.append(anomaly)
    
    # Sort anomalies by severity (Critical first)
    severity_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
    anomalies.sort(key=lambda x: severity_order[x['severity']], reverse=True)
    
    # Generate fake metrics
    metrics = {
        'total_records': random.randint(500, 10000),
        'anomalies_detected': len(anomalies),
        'processing_time': round(random.uniform(1.2, 8.7), 2),
        'baseline_metrics': {
            'precision': round(random.uniform(0.45, 0.65), 3),
            'recall': round(random.uniform(0.52, 0.68), 3),
            'f1_score': 0.600,  # Fixed as requested
            'accuracy': round(random.uniform(0.78, 0.85), 3),
            'false_positive_rate': round(random.uniform(0.12, 0.25), 3)
        },
        'nika_metrics': {
            'precision': round(random.uniform(0.72, 0.85), 3),
            'recall': round(random.uniform(0.74, 0.88), 3),
            'f1_score': 0.780,  # Fixed as requested
            'accuracy': round(random.uniform(0.89, 0.96), 3),
            'false_positive_rate': round(random.uniform(0.03, 0.08), 3)
        },
        'improvement_percentage': {
            'precision': round(((0.780 - 0.600) / 0.600) * 100, 1),
            'recall': round(random.uniform(15.0, 35.0), 1),
            'f1_score': 30.0,  # (0.78 - 0.60) / 0.60 * 100
            'accuracy': round(random.uniform(12.0, 22.0), 1)
        },
        'data_quality': {
            'completeness': round(random.uniform(0.92, 0.99), 3),
            'consistency': round(random.uniform(0.88, 0.96), 3),
            'validity': round(random.uniform(0.90, 0.98), 3)
        },
        'feature_importance': {
            'temperature': round(random.uniform(0.15, 0.25), 3),
            'pressure': round(random.uniform(0.12, 0.22), 3),
            'humidity': round(random.uniform(0.08, 0.18), 3),
            'voltage': round(random.uniform(0.10, 0.20), 3),
            'current': round(random.uniform(0.12, 0.20), 3),
            'speed': round(random.uniform(0.05, 0.15), 3)
        }
    }
    
    return {
        'status': 'success',
        'anomalies': anomalies,
        'metrics': metrics,
        'file_info': {
            'filename': file.name,
            'size_bytes': file.size,
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }


def process_image(file):
    """
    Mock function to process image files and return fake anomaly patches with confidence scores.
    
    Args:
        file: Uploaded image file
        
    Returns:
        dict: Contains anomaly patches, confidence scores, and analysis results
    """
    
    # Generate fake anomaly patches
    patches = []
    num_patches = random.randint(2, 8)
    
    patch_types = [
        'Surface Crack',
        'Corrosion Spot',
        'Discoloration',
        'Texture Anomaly',
        'Foreign Object',
        'Wear Pattern',
        'Deformation',
        'Missing Component',
        'Burn Mark',
        'Contamination'
    ]
    
    # Assume image dimensions for coordinate generation
    img_width = random.randint(800, 2000)
    img_height = random.randint(600, 1500)
    
    for i in range(num_patches):
        patch_width = random.randint(50, 200)
        patch_height = random.randint(50, 200)
        x = random.randint(0, img_width - patch_width)
        y = random.randint(0, img_height - patch_height)
        
        patch = {
            'id': f'patch_{i+1}',
            'type': random.choice(patch_types),
            'confidence': round(random.uniform(0.70, 0.96), 3),
            'severity': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'bounding_box': {
                'x': x,
                'y': y,
                'width': patch_width,
                'height': patch_height
            },
            'center_coordinates': {
                'x': x + patch_width // 2,
                'y': y + patch_height // 2
            },
            'area_percentage': round((patch_width * patch_height) / (img_width * img_height) * 100, 2),
            'color_analysis': {
                'dominant_color': random.choice(['red', 'brown', 'black', 'gray', 'yellow', 'green']),
                'contrast_level': round(random.uniform(0.3, 0.9), 3),
                'brightness': round(random.uniform(0.2, 0.8), 3)
            },
            'texture_features': {
                'roughness': round(random.uniform(0.1, 0.9), 3),
                'uniformity': round(random.uniform(0.2, 0.8), 3),
                'edge_density': round(random.uniform(0.3, 0.9), 3)
            }
        }
        patches.append(patch)
    
    # Sort patches by confidence score (highest first)
    patches.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Generate overall analysis metrics
    analysis_results = {
        'total_patches': len(patches),
        'high_confidence_patches': len([p for p in patches if p['confidence'] > 0.85]),
        'critical_anomalies': len([p for p in patches if p['severity'] == 'Critical']),
        'processing_time': round(random.uniform(2.1, 12.5), 2),
        'image_quality': {
            'resolution': f"{img_width}x{img_height}",
            'clarity_score': round(random.uniform(0.75, 0.95), 3),
            'noise_level': round(random.uniform(0.05, 0.25), 3),
            'contrast_score': round(random.uniform(0.70, 0.90), 3)
        },
        'detection_metrics': {
            'sensitivity': round(random.uniform(0.82, 0.94), 3),
            'specificity': round(random.uniform(0.88, 0.96), 3),
            'precision': round(random.uniform(0.79, 0.91), 3),
            'detection_threshold': round(random.uniform(0.65, 0.75), 3)
        },
        'coverage_analysis': {
            'scanned_area_percentage': round(random.uniform(92.0, 99.5), 1),
            'anomaly_density': round(len(patches) / ((img_width * img_height) / 100000), 3),
            'spatial_distribution': random.choice(['Clustered', 'Scattered', 'Edge-concentrated', 'Center-concentrated'])
        },
        'baseline_comparison': {
            'baseline_detections': random.randint(1, max(1, len(patches) - 2)),
            'nika_detections': len(patches),
            'improvement_rate': round(random.uniform(25.0, 65.0), 1),
            'false_positive_reduction': round(random.uniform(40.0, 70.0), 1)
        }
    }
    
    return {
        'status': 'success',
        'patches': patches,
        'analysis_results': analysis_results,
        'file_info': {
            'filename': file.name,
            'size_bytes': file.size,
            'format': file.name.split('.')[-1].upper(),
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'recommendations': generate_recommendations(patches)
    }


def generate_recommendations(patches):
    """
    Generate recommendations based on detected anomalies.
    
    Args:
        patches: List of detected anomaly patches
        
    Returns:
        list: List of recommendation strings
    """
    recommendations = []
    
    critical_patches = [p for p in patches if p['severity'] == 'Critical']
    high_patches = [p for p in patches if p['severity'] == 'High']
    
    if critical_patches:
        recommendations.append("⚠️ Immediate attention required for critical anomalies detected")
        recommendations.append("🔧 Schedule emergency maintenance for affected areas")
    
    if high_patches:
        recommendations.append("📋 Plan detailed inspection of high-severity anomalies")
    
    if len(patches) > 5:
        recommendations.append("📊 Consider increasing inspection frequency")
    
    patch_types = [p['type'] for p in patches]
    if patch_types.count('Surface Crack') > 1:
        recommendations.append("🔍 Investigate potential structural integrity issues")
    
    if patch_types.count('Corrosion Spot') > 1:
        recommendations.append("🧪 Review environmental conditions and protective measures")
    
    if not recommendations:
        recommendations.append("✅ Overall condition appears satisfactory")
        recommendations.append("📅 Continue with regular inspection schedule")
    
    return recommendations


def generate_report(results, report_type='csv'):
    """
    Generate a PDF report using ReportLab based on analysis results.
    
    Args:
        results: Dict containing analysis results from process_csv or process_image
        report_type: 'csv' or 'image' to determine report format
        
    Returns:
        HttpResponse: PDF file response for download
    """
    if not REPORTLAB_AVAILABLE:
        # Fallback response if ReportLab is not installed
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="report_unavailable.txt"'
        response.write("PDF report generation is not available. Please install ReportLab: pip install reportlab")
        return response
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    # Build PDF content
    story = []
    
    # Title Page
    story.append(Paragraph("NIKA - Intelligent Anomaly Mapping", title_style))
    story.append(Paragraph("Analysis Report", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Report metadata
    metadata_data = [
        ['Report Type:', report_type.upper()],
        ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['File:', results.get('file_info', {}).get('filename', 'N/A')],
        ['Status:', results.get('status', 'Unknown').title()]
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 0.5*inch))
    
    if report_type == 'csv':
        story.extend(_generate_csv_report_content(results, styles, heading_style))
    else:
        story.extend(_generate_image_report_content(results, styles, heading_style))
    
    # Add fake anomaly map
    story.append(PageBreak())
    story.append(Paragraph("Anomaly Distribution Map", heading_style))
    story.append(_create_fake_map_drawing())
    story.append(Spacer(1, 0.3*inch))
    
    # Build PDF
    doc.build(story)
    
    # Return PDF response
    pdf_data = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    filename = f"NIKA_Report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf_data)
    
    return response


def _generate_csv_report_content(results, styles, heading_style):
    """Generate content specific to CSV analysis reports."""
    story = []
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    metrics = results.get('metrics', {})
    
    summary_text = f"""
    NIKA's advanced anomaly detection system has successfully analyzed {metrics.get('total_records', 0):,} records, 
    identifying {metrics.get('anomalies_detected', 0)} anomalies with a processing time of {metrics.get('processing_time', 0)} seconds.
    
    Our system achieved an F1-score of {metrics.get('nika_metrics', {}).get('f1_score', 0)}, representing a 
    {metrics.get('improvement_percentage', {}).get('f1_score', 0)}% improvement over baseline methods.
    """
    
    story.append(Paragraph(summary_text.strip(), styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Performance Metrics Table
    story.append(Paragraph("Performance Metrics Comparison", heading_style))
    
    baseline_metrics = metrics.get('baseline_metrics', {})
    nika_metrics = metrics.get('nika_metrics', {})
    
    metrics_data = [
        ['Metric', 'Baseline', 'NIKA', 'Improvement'],
        ['F1 Score', f"{baseline_metrics.get('f1_score', 0):.3f}", 
         f"{nika_metrics.get('f1_score', 0):.3f}", '+30.0%'],
        ['Precision', f"{baseline_metrics.get('precision', 0):.3f}", 
         f"{nika_metrics.get('precision', 0):.3f}", f"+{random.randint(15, 25)}.0%"],
        ['Recall', f"{baseline_metrics.get('recall', 0):.3f}", 
         f"{nika_metrics.get('recall', 0):.3f}", f"+{random.randint(10, 20)}.0%"],
        ['Accuracy', f"{baseline_metrics.get('accuracy', 0):.3f}", 
         f"{nika_metrics.get('accuracy', 0):.3f}", f"+{random.randint(12, 18)}.0%"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Top Anomalies
    story.append(Paragraph("Critical Anomalies Detected", heading_style))
    
    anomalies = results.get('anomalies', [])[:5]  # Top 5 anomalies
    if anomalies:
        anomaly_data = [['ID', 'Type', 'Severity', 'Confidence', 'Timestamp']]
        for anomaly in anomalies:
            anomaly_data.append([
                anomaly.get('id', 'N/A'),
                anomaly.get('type', 'N/A'),
                anomaly.get('severity', 'N/A'),
                f"{anomaly.get('confidence', 0):.3f}",
                anomaly.get('timestamp', 'N/A')
            ])
        
        anomaly_table = Table(anomaly_data, colWidths=[1*inch, 1.5*inch, 1*inch, 1*inch, 1.5*inch])
        anomaly_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(anomaly_table)
    
    return story


def _generate_image_report_content(results, styles, heading_style):
    """Generate content specific to image analysis reports."""
    story = []
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    analysis = results.get('analysis_results', {})
    
    summary_text = f"""
    NIKA's computer vision system has analyzed the uploaded image, detecting {analysis.get('total_patches', 0)} anomaly patches 
    with {analysis.get('high_confidence_patches', 0)} high-confidence detections. The analysis was completed in 
    {analysis.get('processing_time', 0)} seconds with an overall detection accuracy of 
    {analysis.get('detection_metrics', {}).get('precision', 0):.3f}.
    """
    
    story.append(Paragraph(summary_text.strip(), styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Detection Metrics
    story.append(Paragraph("Detection Performance", heading_style))
    
    detection_metrics = analysis.get('detection_metrics', {})
    image_quality = analysis.get('image_quality', {})
    
    detection_data = [
        ['Metric', 'Score', 'Status'],
        ['Sensitivity', f"{detection_metrics.get('sensitivity', 0):.3f}", 'Excellent'],
        ['Specificity', f"{detection_metrics.get('specificity', 0):.3f}", 'Excellent'],
        ['Precision', f"{detection_metrics.get('precision', 0):.3f}", 'Very Good'],
        ['Image Clarity', f"{image_quality.get('clarity_score', 0):.3f}", 'Good'],
        ['Contrast Score', f"{image_quality.get('contrast_score', 0):.3f}", 'Good']
    ]
    
    detection_table = Table(detection_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    detection_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(detection_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Detected Patches
    story.append(Paragraph("Critical Anomaly Patches", heading_style))
    
    patches = results.get('patches', [])[:5]  # Top 5 patches
    if patches:
        patch_data = [['ID', 'Type', 'Severity', 'Confidence', 'Location']]
        for patch in patches:
            location = f"({patch.get('center_coordinates', {}).get('x', 0)}, {patch.get('center_coordinates', {}).get('y', 0)})"
            patch_data.append([
                patch.get('id', 'N/A'),
                patch.get('type', 'N/A'),
                patch.get('severity', 'N/A'),
                f"{patch.get('confidence', 0):.3f}",
                location
            ])
        
        patch_table = Table(patch_data, colWidths=[1*inch, 1.5*inch, 1*inch, 1*inch, 1.5*inch])
        patch_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c2d12')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(patch_table)
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("Recommendations", heading_style))
        for i, rec in enumerate(recommendations[:3], 1):
            story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
    
    return story


def _create_fake_map_drawing():
    """Create a fake anomaly distribution map using ReportLab graphics."""
    drawing = Drawing(6*inch, 4*inch)
    
    # Background
    drawing.add(Rect(0, 0, 6*inch, 4*inch, fillColor=colors.HexColor('#f8fafc'), strokeColor=colors.gray))
    
    # Grid lines
    for i in range(1, 6):
        x = i * inch
        drawing.add(Rect(x-1, 0, 2, 4*inch, fillColor=colors.HexColor('#e2e8f0'), strokeWidth=0))
    
    for i in range(1, 4):
        y = i * inch
        drawing.add(Rect(0, y-1, 6*inch, 2, fillColor=colors.HexColor('#e2e8f0'), strokeWidth=0))
    
    # Add fake anomaly points
    anomaly_points = [
        (1.2*inch, 3.2*inch, colors.red, 'Critical'),
        (2.8*inch, 2.5*inch, colors.orange, 'High'),
        (4.5*inch, 3.8*inch, colors.red, 'Critical'),
        (1.8*inch, 1.2*inch, colors.yellow, 'Medium'),
        (3.5*inch, 1.8*inch, colors.green, 'Low'),
        (5.2*inch, 2.8*inch, colors.orange, 'High'),
        (0.8*inch, 2.2*inch, colors.yellow, 'Medium'),
        (4.8*inch, 1.5*inch, colors.green, 'Low')
    ]
    
    for x, y, color, severity in anomaly_points:
        # Outer circle (glow effect)
        drawing.add(Circle(x, y, 12, fillColor=color, fillOpacity=0.3, strokeWidth=0))
        # Inner circle
        drawing.add(Circle(x, y, 6, fillColor=color, strokeColor=colors.black, strokeWidth=1))
    
    # Legend
    legend_y = 0.5*inch
    legend_items = [
        (colors.red, 'Critical'),
        (colors.orange, 'High'),
        (colors.yellow, 'Medium'),
        (colors.green, 'Low')
    ]
    
    for i, (color, label) in enumerate(legend_items):
        x = 0.5*inch + i * 1.3*inch
        drawing.add(Circle(x, legend_y, 4, fillColor=color, strokeColor=colors.black, strokeWidth=1))
        drawing.add(String(x + 0.2*inch, legend_y - 3, label, fontSize=8))
    
    return drawing