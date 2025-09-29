import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from django.conf import settings

def generate_anomaly_plots(results):
    """
    Generate matplotlib plots for anomaly detection results.
    
    Args:
        results: Results dictionary from process_csv
        
    Returns:
        dict: Contains base64-encoded plot images
    """
    plots = {}
    
    try:
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Anomaly Severity Distribution
        anomalies = results.get('anomalies', [])
        if anomalies:
            severities = [a.get('severity', 'Unknown') for a in anomalies]
            severity_counts = pd.Series(severities).value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = {'Critical': '#dc2626', 'High': '#ea580c', 'Medium': '#ca8a04', 'Low': '#65a30d'}
            bar_colors = [colors.get(severity, '#6b7280') for severity in severity_counts.index]
            
            bars = ax.bar(severity_counts.index, severity_counts.values, color=bar_colors)
            ax.set_title('Anomaly Severity Distribution', fontsize=14, fontweight='bold')
            ax.set_xlabel('Severity Level')
            ax.set_ylabel('Number of Anomalies')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom')
            
            plt.tight_layout()
            plots['severity_distribution'] = _fig_to_base64(fig)
            plt.close(fig)
        
        # 2. Confidence Score Distribution
        if anomalies:
            confidences = [a.get('confidence', 0) for a in anomalies]
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.hist(confidences, bins=10, color='#3b82f6', alpha=0.7, edgecolor='black')
            ax.set_title('Confidence Score Distribution', fontsize=14, fontweight='bold')
            ax.set_xlabel('Confidence Score')
            ax.set_ylabel('Frequency')
            ax.axvline(np.mean(confidences), color='red', linestyle='--', 
                      label=f'Mean: {np.mean(confidences):.3f}')
            ax.legend()
            
            plt.tight_layout()
            plots['confidence_distribution'] = _fig_to_base64(fig)
            plt.close(fig)
        
        # 3. Performance Comparison
        metrics = results.get('metrics', {})
        baseline = metrics.get('baseline_metrics', {})
        nika = metrics.get('nika_metrics', {})
        
        if baseline and nika:
            metrics_names = ['Precision', 'Recall', 'F1-Score', 'Accuracy']
            baseline_values = [
                baseline.get('precision', 0),
                baseline.get('recall', 0), 
                baseline.get('f1_score', 0),
                baseline.get('accuracy', 0)
            ]
            nika_values = [
                nika.get('precision', 0),
                nika.get('recall', 0),
                nika.get('f1_score', 0), 
                nika.get('accuracy', 0)
            ]
            
            x = np.arange(len(metrics_names))
            width = 0.35
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars1 = ax.bar(x - width/2, baseline_values, width, label='Baseline', color='#ef4444')
            bars2 = ax.bar(x + width/2, nika_values, width, label='NIKA ML', color='#10b981')
            
            ax.set_title('Performance Comparison: Baseline vs NIKA ML', fontsize=14, fontweight='bold')
            ax.set_xlabel('Metrics')
            ax.set_ylabel('Score')
            ax.set_xticks(x)
            ax.set_xticklabels(metrics_names)
            ax.legend()
            ax.set_ylim(0, 1)
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           f'{height:.3f}', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            plots['performance_comparison'] = _fig_to_base64(fig)
            plt.close(fig)
        
        # 4. Anomaly Timeline (mock data based on timestamps)
        if anomalies:
            # Create mock timeline data
            timestamps = []
            for a in anomalies:
                try:
                    from datetime import datetime
                    ts = datetime.strptime(a.get('timestamp', ''), '%Y-%m-%d %H:%M:%S')
                    timestamps.append(ts)
                except:
                    continue
            
            if timestamps:
                # Group by hour
                hours = [ts.hour for ts in timestamps]
                hour_counts = pd.Series(hours).value_counts().sort_index()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(hour_counts.index, hour_counts.values, marker='o', linewidth=2, markersize=6)
                ax.set_title('Anomaly Detection Timeline (by Hour)', fontsize=14, fontweight='bold')
                ax.set_xlabel('Hour of Day')
                ax.set_ylabel('Number of Anomalies')
                ax.grid(True, alpha=0.3)
                ax.set_xticks(range(0, 24, 2))
                
                plt.tight_layout()
                plots['timeline'] = _fig_to_base64(fig)
                plt.close(fig)
        
    except Exception as e:
        print(f"Error generating plots: {e}")
    
    return plots

def generate_image_plots(results):
    """
    Generate matplotlib plots for image analysis results.
    
    Args:
        results: Results dictionary from process_image
        
    Returns:
        dict: Contains base64-encoded plot images
    """
    plots = {}
    
    try:
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        anomaly_zones = results.get('anomaly_zones', [])
        
        # 1. Confidence by Mineral Type
        if anomaly_zones:
            mineral_types = [zone.get('mineral_type', 'Unknown') for zone in anomaly_zones]
            confidences = [zone.get('confidence', 0) for zone in anomaly_zones]
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ['#e11d48', '#059669', '#dc2626', '#7c3aed', '#ea580c']
            bars = ax.bar(mineral_types, confidences, color=colors[:len(mineral_types)])
            
            ax.set_title('Mineral Detection Confidence', fontsize=14, fontweight='bold')
            ax.set_xlabel('Mineral Type')
            ax.set_ylabel('Confidence Score')
            ax.set_ylim(0, 1)
            
            # Add value labels
            for bar, conf in zip(bars, confidences):
                ax.text(bar.get_x() + bar.get_width()/2., conf + 0.02,
                       f'{conf:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plots['mineral_confidence'] = _fig_to_base64(fig)
            plt.close(fig)
        
        # 2. Zone Area Distribution
        if anomaly_zones:
            areas = []
            zone_names = []
            for zone in anomaly_zones:
                bbox = zone.get('bounding_box', {})
                area = bbox.get('width', 0) * bbox.get('height', 0)
                areas.append(area)
                zone_names.append(zone.get('name', 'Zone'))
            
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#ef4444', '#10b981', '#3b82f6']
            wedges, texts, autotexts = ax.pie(areas, labels=zone_names, autopct='%1.1f%%', 
                                            colors=colors, startangle=90)
            
            ax.set_title('Anomaly Zone Area Distribution', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plots['area_distribution'] = _fig_to_base64(fig)
            plt.close(fig)
        
        # 3. ML Metrics Radar Chart
        analysis = results.get('analysis_results', {})
        detection_metrics = analysis.get('detection_metrics', {})
        
        if detection_metrics:
            metrics = ['Sensitivity', 'Specificity', 'Precision']
            values = [
                detection_metrics.get('sensitivity', 0),
                detection_metrics.get('specificity', 0),
                detection_metrics.get('precision', 0)
            ]
            
            # Add first value to end to close the circle
            values += values[:1]
            
            angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            ax.plot(angles, values, 'o-', linewidth=2, color='#3b82f6')
            ax.fill(angles, values, alpha=0.25, color='#3b82f6')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(metrics)
            ax.set_ylim(0, 1)
            ax.set_title('ML Detection Metrics', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True)
            
            plt.tight_layout()
            plots['ml_metrics_radar'] = _fig_to_base64(fig)
            plt.close(fig)
        
    except Exception as e:
        print(f"Error generating image plots: {e}")
    
    return plots

def _fig_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic