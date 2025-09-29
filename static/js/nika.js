// NIKA Dashboard JavaScript - Modern Interactive Features

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
    }

    setupThemeToggle() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }
}

// File Upload Manager
class FileUploadManager {
    constructor() {
        this.setupUploadAreas();
        this.setupProgressBars();
    }

    setupUploadAreas() {
        const uploadAreas = document.querySelectorAll('.upload-area');
        uploadAreas.forEach(area => {
            this.setupDragAndDrop(area);
            this.setupFileInput(area);
        });
    }

    setupDragAndDrop(area) {
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });

        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });

        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0], area);
            }
        });
    }

    setupFileInput(area) {
        const fileInput = area.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileUpload(e.target.files[0], area);
                }
            });
        }
    }

    handleFileUpload(file, area) {
        const maxSize = 50 * 1024 * 1024; // 50MB
        
        if (file.size > maxSize) {
            this.showAlert('File size too large. Maximum 50MB allowed.', 'error');
            return;
        }

        // Validate file type
        const fileType = area.dataset.fileType;
        if (fileType === 'csv' && !file.type.includes('csv') && !file.name.endsWith('.csv')) {
            this.showAlert('Please upload a CSV file.', 'error');
            return;
        }
        
        if (fileType === 'image' && !file.type.startsWith('image/')) {
            this.showAlert('Please upload an image file.', 'error');
            return;
        }

        this.uploadFile(file, area);
    }

    uploadFile(file, area) {
        const formData = new FormData();
        const fileType = area.dataset.fileType;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        formData.append(`${fileType}_file`, file);
        formData.append('csrfmiddlewaretoken', csrfToken);
        
        const progressBar = area.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = '0%';
        }

        // Create XMLHttpRequest for progress tracking
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable && progressBar) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        this.showAlert(`${file.name} uploaded successfully!`, 'success');
                        this.handleUploadSuccess(response, fileType);
                    } else {
                        this.showAlert(response.error || 'Upload failed', 'error');
                    }
                } catch (e) {
                    // If not JSON response, redirect to results page
                    window.location.reload();
                }
            } else {
                this.showAlert('Upload failed. Please try again.', 'error');
            }
        });

        xhr.addEventListener('error', () => {
            this.showAlert('Upload failed. Please check your connection.', 'error');
        });

        const uploadUrl = fileType === 'csv' ? '/upload-csv/' : '/upload-image/';
        xhr.open('POST', uploadUrl);
        xhr.send(formData);
    }

    handleUploadSuccess(response, fileType) {
        // Update UI based on successful upload
        if (fileType === 'csv') {
            this.updateCSVResults(response.data);
        } else if (fileType === 'image') {
            this.updateImageResults(response.data);
        }
    }

    updateCSVResults(data) {
        // Update CSV results section
        const resultsSection = document.getElementById('csv-results');
        if (resultsSection && data) {
            this.displayCSVMetrics(data.metrics);
            this.displayAnomalies(data.anomalies);
            this.showTab('csv-results');
        }
    }

    updateImageResults(data) {
        // Update image results section
        const resultsSection = document.getElementById('image-results');
        if (resultsSection && data) {
            this.displayImageAnalysis(data);
            this.showTab('image-results');
        }
    }

    displayCSVMetrics(metrics) {
        const metricsContainer = document.getElementById('csv-metrics');
        if (metricsContainer && metrics) {
            metricsContainer.innerHTML = `
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">${metrics.total_rows || 0}</div>
                        <div class="metric-label">Total Rows</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${metrics.anomalies_found || 0}</div>
                        <div class="metric-label">Anomalies Found</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${metrics.confidence_score || '0'}%</div>
                        <div class="metric-label">Confidence Score</div>
                    </div>
                </div>
            `;
        }
    }

    displayAnomalies(anomalies) {
        const anomaliesContainer = document.getElementById('anomalies-list');
        if (anomaliesContainer && anomalies) {
            const anomaliesHTML = anomalies.map(anomaly => `
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">${anomaly.type}</h4>
                        <span class="badge ${this.getSeverityClass(anomaly.severity)}">${anomaly.severity}</span>
                    </div>
                    <div class="card-content">
                        <p>${anomaly.description}</p>
                        <div class="flex justify-between items-center mt-2">
                            <span class="text-sm text-muted">Row: ${anomaly.row}</span>
                            <span class="text-sm font-medium">Confidence: ${anomaly.confidence}%</span>
                        </div>
                    </div>
                </div>
            `).join('');
            
            anomaliesContainer.innerHTML = anomaliesHTML;
        }
    }

    displayImageAnalysis(data) {
        const imageContainer = document.getElementById('image-analysis');
        if (imageContainer && data) {
            imageContainer.innerHTML = `
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="card-title">Original Image</h4>
                        </div>
                        <div class="card-content">
                            <img src="${data.original_image}" alt="Original" class="w-full rounded">
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header">
                            <h4 class="card-title">Anomaly Overlay</h4>
                        </div>
                        <div class="card-content">
                            <img src="${data.overlay_image}" alt="Overlay" class="w-full rounded">
                        </div>
                    </div>
                </div>
                <div class="metrics-grid mt-6">
                    <div class="metric-card">
                        <div class="metric-value">${data.anomalies_detected || 0}</div>
                        <div class="metric-label">Anomalies Detected</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${data.confidence_score || '0'}%</div>
                        <div class="metric-label">Confidence Score</div>
                    </div>
                </div>
            `;
        }
    }

    getSeverityClass(severity) {
        const severityClasses = {
            'High': 'bg-red-500',
            'Medium': 'bg-yellow-500',
            'Low': 'bg-green-500'
        };
        return severityClasses[severity] || 'bg-gray-500';
    }

    setupProgressBars() {
        // Initialize progress bars to 0%
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            bar.style.width = '0%';
        });
    }

    showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" class="btn btn-sm">×</button>
        `;
        
        // Add to alerts container or top of page
        const alertsContainer = document.getElementById('alerts-container');
        const targetContainer = alertsContainer || document.body;
        
        if (alertsContainer) {
            alertsContainer.appendChild(alertDiv);
        } else {
            targetContainer.insertBefore(alertDiv, targetContainer.firstChild);
        }
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentElement) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Tab Management
class TabManager {
    constructor() {
        this.init();
    }

    init() {
        const tabButtons = document.querySelectorAll('.tab-button');
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tabId = button.dataset.tab;
                this.showTab(tabId);
            });
        });
    }

    showTab(tabId) {
        // Hide all tab contents
        const tabContents = document.querySelectorAll('.tab-content');
        tabContents.forEach(content => {
            content.classList.remove('active');
        });

        // Remove active class from all tab buttons
        const tabButtons = document.querySelectorAll('.tab-button');
        tabButtons.forEach(button => {
            button.classList.remove('active');
        });

        // Show selected tab content
        const selectedContent = document.getElementById(tabId);
        if (selectedContent) {
            selectedContent.classList.add('active');
        }

        // Activate selected tab button
        const selectedButton = document.querySelector(`[data-tab="${tabId}"]`);
        if (selectedButton) {
            selectedButton.classList.add('active');
        }
    }
}

// Chart Manager (using Chart.js if available)
class ChartManager {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        // Initialize charts when Chart.js is available
        if (typeof Chart !== 'undefined') {
            this.initializeCharts();
        } else {
            // Load Chart.js dynamically
            this.loadChartJS().then(() => {
                this.initializeCharts();
            });
        }
    }

    loadChartJS() {
        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.onload = resolve;
            document.head.appendChild(script);
        });
    }

    initializeCharts() {
        this.createAnomalyChart();
        this.createTrendChart();
    }

    createAnomalyChart() {
        const ctx = document.getElementById('anomaly-chart');
        if (ctx && !this.charts.anomaly) {
            this.charts.anomaly = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Normal Data', 'Anomalies'],
                    datasets: [{
                        data: [85, 15],
                        backgroundColor: ['#10b981', '#ef4444'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: getComputedStyle(document.documentElement)
                                    .getPropertyValue('--foreground')
                            }
                        }
                    }
                }
            });
        }
    }

    createTrendChart() {
        const ctx = document.getElementById('trend-chart');
        if (ctx && !this.charts.trend) {
            this.charts.trend = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Anomalies Detected',
                        data: [12, 19, 3, 17, 6, 3],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: getComputedStyle(document.documentElement)
                                    .getPropertyValue('--border')
                            },
                            ticks: {
                                color: getComputedStyle(document.documentElement)
                                    .getPropertyValue('--muted-foreground')
                            }
                        },
                        x: {
                            grid: {
                                color: getComputedStyle(document.documentElement)
                                    .getPropertyValue('--border')
                            },
                            ticks: {
                                color: getComputedStyle(document.documentElement)
                                    .getPropertyValue('--muted-foreground')
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: getComputedStyle(document.documentElement)
                                    .getPropertyValue('--foreground')
                            }
                        }
                    }
                }
            });
        }
    }

    updateChart(chartId, data) {
        if (this.charts[chartId]) {
            this.charts[chartId].data = data;
            this.charts[chartId].update();
        }
    }
}

// Map Manager (using Leaflet.js if available)
class MapManager {
    constructor() {
        this.maps = {};
        this.init();
    }

    init() {
        if (typeof L !== 'undefined') {
            this.initializeMaps();
        } else {
            this.loadLeaflet().then(() => {
                this.initializeMaps();
            });
        }
    }

    loadLeaflet() {
        return Promise.all([
            this.loadCSS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'),
            this.loadJS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js')
        ]);
    }

    loadCSS(url) {
        return new Promise((resolve) => {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = url;
            link.onload = resolve;
            document.head.appendChild(link);
        });
    }

    loadJS(url) {
        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = url;
            script.onload = resolve;
            document.head.appendChild(script);
        });
    }

    initializeMaps() {
        const mapContainers = document.querySelectorAll('.map-container[id]');
        mapContainers.forEach(container => {
            this.createMap(container.id);
        });
    }

    createMap(containerId) {
        const container = document.getElementById(containerId);
        if (container && !this.maps[containerId]) {
            // Default coordinates (can be updated with real data)
            const map = L.map(containerId).setView([40.7128, -74.0060], 10);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            // Add sample markers
            this.addSampleMarkers(map);
            
            this.maps[containerId] = map;
        }
    }

    addSampleMarkers(map) {
        // Sample anomaly locations
        const anomalies = [
            { lat: 40.7128, lng: -74.0060, severity: 'High', type: 'Chemical Anomaly' },
            { lat: 40.7589, lng: -73.9851, severity: 'Medium', type: 'Temperature Spike' },
            { lat: 40.6892, lng: -74.0445, severity: 'Low', type: 'pH Variation' }
        ];

        anomalies.forEach(anomaly => {
            const color = anomaly.severity === 'High' ? 'red' : 
                         anomaly.severity === 'Medium' ? 'orange' : 'yellow';
            
            const marker = L.circleMarker([anomaly.lat, anomaly.lng], {
                color: color,
                fillColor: color,
                fillOpacity: 0.7,
                radius: 8
            }).addTo(map);

            marker.bindPopup(`
                <strong>${anomaly.type}</strong><br>
                Severity: ${anomaly.severity}<br>
                Lat: ${anomaly.lat.toFixed(4)}<br>
                Lng: ${anomaly.lng.toFixed(4)}
            `);
        });
    }

    addAnomalyMarkers(mapId, anomalies) {
        const map = this.maps[mapId];
        if (map && anomalies) {
            // Clear existing markers
            map.eachLayer(layer => {
                if (layer instanceof L.CircleMarker) {
                    map.removeLayer(layer);
                }
            });

            // Add new markers
            anomalies.forEach(anomaly => {
                if (anomaly.latitude && anomaly.longitude) {
                    const marker = L.circleMarker([anomaly.latitude, anomaly.longitude], {
                        color: this.getSeverityColor(anomaly.severity),
                        fillColor: this.getSeverityColor(anomaly.severity),
                        fillOpacity: 0.7,
                        radius: 8
                    }).addTo(map);

                    marker.bindPopup(`
                        <strong>${anomaly.type}</strong><br>
                        ${anomaly.description}<br>
                        Confidence: ${anomaly.confidence}%
                    `);
                }
            });
        }
    }

    getSeverityColor(severity) {
        const colors = {
            'High': '#ef4444',
            'Medium': '#f59e0b',
            'Low': '#10b981'
        };
        return colors[severity] || '#6b7280';
    }
}

// Mobile Menu Manager
class MobileMenuManager {
    constructor() {
        this.init();
    }

    init() {
        const menuToggle = document.getElementById('mobile-menu-toggle');
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebar-overlay');

        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('open');
                if (overlay) {
                    overlay.style.display = sidebar.classList.contains('open') ? 'block' : 'none';
                }
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.style.display = 'none';
            });
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers
    const themeManager = new ThemeManager();
    const fileUploadManager = new FileUploadManager();
    const tabManager = new TabManager();
    const chartManager = new ChartManager();
    const mapManager = new MapManager();
    const mobileMenuManager = new MobileMenuManager();

// Image Analysis Manager
class ImageAnalysisManager {
    constructor() {
        this.overlayVisible = false;
        this.canvas = null;
        this.ctx = null;
        this.image = null;
        this.init();
    }
    
    init() {
        this.setupOverlayCanvas();
        this.setupZoneInteractions();
        this.setupOverlayToggle();
    }
    
    setupOverlayCanvas() {
        this.canvas = document.getElementById('anomaly-overlay');
        this.image = document.getElementById('main-image');
        
        if (!this.canvas || !this.image) return;
        
        this.ctx = this.canvas.getContext('2d');
        
        // Wait for image to load, then set canvas dimensions
        if (this.image.complete) {
            this.resizeCanvas();
        } else {
            this.image.addEventListener('load', () => this.resizeCanvas());
        }
        
        // Handle window resize
        window.addEventListener('resize', () => this.resizeCanvas());
    }
    
    resizeCanvas() {
        if (!this.canvas || !this.image) return;
        
        const rect = this.image.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        
        if (this.overlayVisible) {
            this.drawAnomalyZones();
        }
    }
    
    setupOverlayToggle() {
        const toggleBtn = document.getElementById('toggle-overlay');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleOverlay());
        }
    }
    
    toggleOverlay() {
        this.overlayVisible = !this.overlayVisible;
        
        if (this.overlayVisible) {
            this.canvas.style.display = 'block';
            this.drawAnomalyZones();
        } else {
            this.canvas.style.display = 'none';
        }
        
        // Update button icon and text
        const toggleBtn = document.getElementById('toggle-overlay');
        const icon = toggleBtn.querySelector('i');
        if (this.overlayVisible) {
            icon.setAttribute('data-lucide', 'eye-off');
            toggleBtn.querySelector('span') && (toggleBtn.querySelector('span').textContent = 'Hide Overlay');
        } else {
            icon.setAttribute('data-lucide', 'eye');
            toggleBtn.querySelector('span') && (toggleBtn.querySelector('span').textContent = 'Show Overlay');
        }
        
        // Re-initialize lucide icons
        if (window.lucide) {
            lucide.createIcons();
        }
    }
    
    drawAnomalyZones() {
        if (!this.ctx || !this.canvas) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Get zone data from DOM
        const zones = document.querySelectorAll('.zone-item');
        const imageRect = this.image.getBoundingClientRect();
        const canvasRect = this.canvas.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = this.canvas.width / this.image.naturalWidth;
        const scaleY = this.canvas.height / this.image.naturalHeight;
        
        zones.forEach((zone, index) => {
            const x = parseInt(zone.dataset.x) * scaleX;
            const y = parseInt(zone.dataset.y) * scaleY;
            const width = parseInt(zone.dataset.width) * scaleX;
            const height = parseInt(zone.dataset.height) * scaleY;
            
            // Generate color based on zone index
            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'];
            const color = colors[index % colors.length];
            
            // Draw bounding box
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 3;
            this.ctx.strokeRect(x, y, width, height);
            
            // Draw semi-transparent fill
            this.ctx.fillStyle = color + '20';
            this.ctx.fillRect(x, y, width, height);
            
            // Draw zone label
            this.ctx.fillStyle = color;
            this.ctx.font = '14px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
            this.ctx.fillText(`Zone ${index + 1}`, x + 5, y + 20);
        });
    }
    
    setupZoneInteractions() {
        const zones = document.querySelectorAll('.zone-item');
        zones.forEach((zone, index) => {
            zone.addEventListener('mouseenter', () => this.highlightZone(index));
            zone.addEventListener('mouseleave', () => this.unhighlightZone(index));
            zone.addEventListener('click', () => this.focusZone(index));
        });
    }
    
    highlightZone(index) {
        if (!this.overlayVisible) return;
        
        const zone = document.querySelectorAll('.zone-item')[index];
        zone.style.backgroundColor = 'var(--muted)';
        
        // Redraw with highlighted zone
        this.drawAnomalyZones();
    }
    
    unhighlightZone(index) {
        const zone = document.querySelectorAll('.zone-item')[index];
        zone.style.backgroundColor = '';
    }
    
    focusZone(index) {
        if (!this.overlayVisible) {
            this.toggleOverlay();
        }
        
        // Scroll to zone in the list
        const zone = document.querySelectorAll('.zone-item')[index];
        zone.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// PDF Report Download Function
window.downloadImageReport = function() {
    // Create a form to submit the image results for PDF generation
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/download-image-report/';
    
    // Add CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken.value;
        form.appendChild(csrfInput);
    }
    
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
};

// Make managers globally accessible for debugging
window.NIKA = {
    theme: themeManager,
    upload: fileUploadManager,
    tabs: tabManager,
    charts: chartManager,
    maps: mapManager,
    mobile: mobileMenuManager,
    imageAnalysis: new ImageAnalysisManager()
};

    // Initialize default tab
    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('tab');
    
    if (activeTab) {
        const tabButton = document.querySelector(`.tab-button[data-tab="${activeTab}"]`);
        if (tabButton) {
            tabButton.click();
        }
    } else {
        // Check if we have results to show and auto-switch
        const hasImageResults = document.querySelector('#image-results .card .card-content img');
        const hasCsvResults = document.querySelector('#csv-results table tbody tr');
        
        if (hasImageResults) {
            // Switch to image results tab if we have image results
            const imageTab = document.querySelector('.tab-button[data-tab="image-results"]');
            if (imageTab) {
                imageTab.click();
            }
        } else if (hasCsvResults) {
            // Switch to CSV results tab if we have CSV results
            const csvTab = document.querySelector('.tab-button[data-tab="csv-results"]');
            if (csvTab) {
                csvTab.click();
            }
        } else {
            // Default to upload tab
            const defaultTab = document.querySelector('.tab-button[data-tab="upload"]');
            if (defaultTab) {
                defaultTab.click();
            }
        }
    }

    // Auto-hide alerts after page load
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.parentElement) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }
        });
    }, 3000);
});

// Global utility functions
window.showTab = function(tabId) {
    if (window.NIKA && window.NIKA.tabs) {
        window.NIKA.tabs.showTab(tabId);
    }
};

window.downloadReport = function() {
    window.location.href = '/download-report/';
};

// Error handling
window.addEventListener('error', (e) => {
    console.error('NIKA Dashboard Error:', e.error);
});

// Service Worker registration for offline support (if available)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/sw.js')
        .then(() => console.log('Service Worker registered'))
        .catch(() => console.log('Service Worker registration failed'));
}