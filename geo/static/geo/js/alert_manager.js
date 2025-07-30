/**
 * Professional Alert Management System
 * Smart For Green - Fire Detection Alert Manager
 * 
 * Features:
 * - Professional sliding alert panel
 * - Advanced alert filtering and sorting
 * - Sound notifications
 * - Alert priority levels
 * - Real-time statistics
 * - Export functionality
 */

class AlertManager {
    constructor() {
        this.alerts = [];
        this.isInitialized = false;
        this.soundEnabled = true;
        this.notificationPermission = 'default';
        this.filterSettings = {
            status: 'all', // all, active, resolved
            priority: 'all', // all, high, medium, low
            timeRange: 'all' // all, 1h, 24h, 7d
        };
        
        this.init();
    }

    async init() {
        if (this.isInitialized) return;
        
        await this.requestNotificationPermission();
        this.createAlertManagerUI();
        this.bindEventListeners();
        this.initializeStatusIndicator();
        this.loadSettings();
        
        this.isInitialized = true;
        console.log('🚀 Professional Alert Manager initialized');
    }

    // Request browser notification permission
    async requestNotificationPermission() {
        if ('Notification' in window) {
            this.notificationPermission = await Notification.requestPermission();
        }
    }

    // Create the professional alert manager UI
    createAlertManagerUI() {
        // Create alert manager button in header
        this.createAlertButton();
        
        // Create sliding alert panel
        this.createAlertPanel();
        
        // Create status indicator
        this.createStatusIndicator();
        
        // Create sound toggle
        this.createSoundToggle();
    }

    createAlertButton() {
        const pageHeader = document.querySelector('.page-header');
        if (!pageHeader) return;

        const alertButton = document.createElement('div');
        alertButton.className = 'alert-manager-button';
        alertButton.innerHTML = `
            <button id="alert-manager-btn" class="btn btn-danger position-relative">
                <i class="fas fa-fire"></i>
                <span class="ms-2">Alerts</span>
                <span id="alert-badge" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning" style="display: none;">
                    0
                </span>
            </button>
        `;
        
        pageHeader.appendChild(alertButton);
    }

    createAlertPanel() {
        const alertPanel = document.createElement('div');
        alertPanel.id = 'alert-panel';
        alertPanel.className = 'alert-panel';
        alertPanel.innerHTML = `
            <div class="alert-panel-header">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                        <i class="fas fa-fire text-danger me-2"></i>
                        Fire Alert Manager
                    </h5>
                    <button id="close-alert-panel" class="btn btn-sm btn-outline-secondary">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <!-- Alert Statistics -->
                <div class="alert-stats mt-3">
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="stat-item">
                                <div class="stat-number text-danger" id="total-alerts">0</div>
                                <div class="stat-label">Total</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="stat-item">
                                <div class="stat-number text-warning" id="active-alerts">0</div>
                                <div class="stat-label">Active</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="stat-item">
                                <div class="stat-number text-success" id="resolved-alerts">0</div>
                                <div class="stat-label">Resolved</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Alert Filters -->
            <div class="alert-filters">
                <div class="row g-2">
                    <div class="col-4">
                        <select id="status-filter" class="form-select form-select-sm">
                            <option value="all">All Status</option>
                            <option value="active">Active</option>
                            <option value="resolved">Resolved</option>
                        </select>
                    </div>
                    <div class="col-4">
                        <select id="priority-filter" class="form-select form-select-sm">
                            <option value="all">All Priority</option>
                            <option value="high">High</option>
                            <option value="medium">Medium</option>
                            <option value="low">Low</option>
                        </select>
                    </div>
                    <div class="col-4">
                        <select id="time-filter" class="form-select form-select-sm">
                            <option value="all">All Time</option>
                            <option value="1h">Last Hour</option>
                            <option value="24h">Last 24h</option>
                            <option value="7d">Last 7 days</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Alert List -->
            <div class="alert-list-container">
                <div id="professional-alerts-list" class="professional-alerts-list">
                    <div id="no-alerts-professional" class="no-alerts-message">
                        <div class="text-center text-muted py-4">
                            <i class="fas fa-shield-alt fa-2x mb-2"></i>
                            <p>No fire alerts detected</p>
                            <small>System is monitoring and ready</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Alert Actions -->
            <div class="alert-actions">
                <button id="resolve-all-alerts" class="btn btn-sm btn-success me-2">
                    <i class="fas fa-check"></i> Resolve All
                </button>
                <button id="export-alerts" class="btn btn-sm btn-outline-primary me-2">
                    <i class="fas fa-download"></i> Export
                </button>
                <button id="test-professional-alert" class="btn btn-sm btn-outline-warning">
                    <i class="fas fa-vial"></i> Test Alert
                </button>
            </div>
        `;

        document.body.appendChild(alertPanel);
    }

    createStatusIndicator() {
        const statusIndicator = document.createElement('div');
        statusIndicator.id = 'connection-status-indicator';
        statusIndicator.className = 'connection-status-indicator';
        statusIndicator.innerHTML = `
            <div class="status-content">
                <span class="status-dot"></span>
                <span class="status-text">Connecting...</span>
            </div>
        `;
        
        document.body.appendChild(statusIndicator);
    }

    createSoundToggle() {
        const soundToggle = document.createElement('div');
        soundToggle.id = 'sound-toggle';
        soundToggle.className = 'sound-toggle';
        soundToggle.innerHTML = `
            <button id="sound-toggle-btn" class="btn btn-sm btn-outline-secondary" title="Toggle Alert Sounds">
                <i class="fas fa-volume-up"></i>
            </button>
        `;
        
        const alertPanel = document.getElementById('alert-panel');
        if (alertPanel) {
            const header = alertPanel.querySelector('.alert-panel-header');
            header.appendChild(soundToggle);
        }
    }

    bindEventListeners() {
        // Alert manager button
        const alertBtn = document.getElementById('alert-manager-btn');
        if (alertBtn) {
            alertBtn.addEventListener('click', () => this.toggleAlertPanel());
        }

        // Close panel button
        const closeBtn = document.getElementById('close-alert-panel');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hideAlertPanel());
        }

        // Filter listeners
        const statusFilter = document.getElementById('status-filter');
        const priorityFilter = document.getElementById('priority-filter');
        const timeFilter = document.getElementById('time-filter');

        if (statusFilter) statusFilter.addEventListener('change', (e) => this.applyFilters());
        if (priorityFilter) priorityFilter.addEventListener('change', (e) => this.applyFilters());
        if (timeFilter) timeFilter.addEventListener('change', (e) => this.applyFilters());

        // Action buttons
        const resolveAllBtn = document.getElementById('resolve-all-alerts');
        const exportBtn = document.getElementById('export-alerts');
        const testBtn = document.getElementById('test-professional-alert');

        if (resolveAllBtn) resolveAllBtn.addEventListener('click', () => this.resolveAllAlerts());
        if (exportBtn) exportBtn.addEventListener('click', () => this.exportAlerts());
        if (testBtn) testBtn.addEventListener('click', () => this.testAlert());

        // Sound toggle
        const soundToggleBtn = document.getElementById('sound-toggle-btn');
        if (soundToggleBtn) {
            soundToggleBtn.addEventListener('click', () => this.toggleSound());
        }

        // Click outside to close panel
        document.addEventListener('click', (e) => {
            const panel = document.getElementById('alert-panel');
            const button = document.getElementById('alert-manager-btn');
            
            if (panel && !panel.contains(e.target) && !button?.contains(e.target)) {
                this.hideAlertPanel();
            }
        });
    }

    // Add new alert with enhanced features
    addAlert(alertData) {
        const alert = {
            id: alertData.id || Date.now() + Math.random(),
            ...alertData,
            status: alertData.is_resolved ? 'resolved' : 'active',
            priority: this.calculatePriority(alertData.confidence),
            timestamp: new Date(alertData.timestamp || Date.now()),
            resolved: alertData.is_resolved || false
        };

        this.alerts.unshift(alert);
        this.renderAlert(alert);
        this.updateStatistics();
        this.playAlertSound();
        this.showBrowserNotification(alert);
        this.updateBadge();

        // Auto-save to localStorage
        this.saveToStorage();

        // Sync with backend if this is a new alert
        if (!alertData.id) {
            this.syncAlertToBackend(alert);
        }
    }

    // Sync alert to backend
    async syncAlertToBackend(alert) {
        try {
            const response = await fetch('/api/fire-alerts/webhook/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    camera_id: alert.camera_id,
                    farm_id: alert.farm_id,
                    confidence: alert.confidence,
                    timestamp: alert.timestamp.toISOString(),
                    notes: alert.notes || 'Generated from alert manager'
                })
            });

            if (response.ok) {
                const data = await response.json();
                alert.id = data.alert_id; // Update with backend ID
                console.log('✅ Alert synced to backend:', data);
            }
        } catch (error) {
            console.error('❌ Failed to sync alert to backend:', error);
        }
    }

    calculatePriority(confidence) {
        if (confidence >= 0.9) return 'high';
        if (confidence >= 0.7) return 'medium';
        return 'low';
    }

    renderAlert(alert) {
        const alertsList = document.getElementById('professional-alerts-list');
        const noAlertsMsg = document.getElementById('no-alerts-professional');
        
        if (noAlertsMsg) noAlertsMsg.style.display = 'none';

        const alertElement = document.createElement('div');
        alertElement.className = `professional-alert-item ${alert.priority}-priority ${alert.status}`;
        alertElement.dataset.alertId = alert.id;

        const priorityIcon = {
            high: 'fas fa-exclamation-triangle',
            medium: 'fas fa-exclamation-circle',
            low: 'fas fa-info-circle'
        };

        const priorityColor = {
            high: 'text-danger',
            medium: 'text-warning',
            low: 'text-info'
        };

        alertElement.innerHTML = `
            <div class="alert-item-header">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="alert-title">
                        <i class="${priorityIcon[alert.priority]} ${priorityColor[alert.priority]} me-2"></i>
                        <span class="fw-bold">Fire Detected</span>
                        <span class="badge bg-${alert.priority === 'high' ? 'danger' : alert.priority === 'medium' ? 'warning' : 'info'} ms-2">
                            ${alert.priority.toUpperCase()}
                        </span>
                    </div>
                    <div class="alert-actions-mini">
                        <button class="btn btn-sm btn-outline-success me-1" onclick="alertManager.resolveAlert('${alert.id}')" title="Resolve">
                            <i class="fas fa-check"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="alertManager.deleteAlert('${alert.id}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="alert-item-body">
                <div class="row">
                    <div class="col-6">
                        <small class="text-muted">Camera ID</small>
                        <div class="fw-semibold">${alert.camera_id || 'Unknown'}</div>
                    </div>
                    <div class="col-6">
                        <small class="text-muted">Farm ID</small>
                        <div class="fw-semibold">${alert.farm_id || 'Unknown'}</div>
                    </div>
                </div>
                
                <div class="row mt-2">
                    <div class="col-6">
                        <small class="text-muted">Confidence</small>
                        <div class="fw-semibold">${(alert.confidence * 100).toFixed(1)}%</div>
                    </div>
                    <div class="col-6">
                        <small class="text-muted">Time</small>
                        <div class="fw-semibold">${alert.timestamp.toLocaleTimeString()}</div>
                    </div>
                </div>
                
                <div class="alert-timestamp text-muted mt-2">
                    <i class="fas fa-clock me-1"></i>
                    ${this.formatTimestamp(alert.timestamp)}
                </div>
            </div>
        `;

        alertsList.insertBefore(alertElement, alertsList.firstChild);
    }

    formatTimestamp(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
        return timestamp.toLocaleDateString();
    }

    resolveAlert(alertId) {
        const alert = this.alerts.find(a => a.id.toString() === alertId.toString());
        if (alert) {
            alert.status = 'resolved';
            alert.resolved = true;
            
            const element = document.querySelector(`[data-alert-id="${alertId}"]`);
            if (element) {
                element.classList.remove('active');
                element.classList.add('resolved');
            }
            
            this.updateStatistics();
            this.saveToStorage();

            // Sync with backend
            this.syncResolveToBackend(alertId);
        }
    }

    // Sync resolve action to backend
    async syncResolveToBackend(alertId) {
        try {
            const response = await fetch(`/api/fire-alerts/${alertId}/resolve/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    notes: 'Resolved from alert manager'
                })
            });

            if (response.ok) {
                console.log('✅ Alert resolved in backend');
            }
        } catch (error) {
            console.error('❌ Failed to sync resolve to backend:', error);
        }
    }

    deleteAlert(alertId) {
        this.alerts = this.alerts.filter(a => a.id.toString() !== alertId.toString());
        
        const element = document.querySelector(`[data-alert-id="${alertId}"]`);
        if (element) {
            element.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => element.remove(), 300);
        }
        
        this.updateStatistics();
        this.updateBadge();
        this.saveToStorage();
        this.checkIfNoAlerts();

        // Sync with backend
        this.syncDeleteToBackend(alertId);
    }

    // Sync delete action to backend
    async syncDeleteToBackend(alertId) {
        try {
            const response = await fetch(`/api/fire-alerts/${alertId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                console.log('✅ Alert deleted from backend');
            }
        } catch (error) {
            console.error('❌ Failed to sync delete to backend:', error);
        }
    }

    resolveAllAlerts() {
        this.alerts.forEach(alert => {
            if (alert.status === 'active') {
                alert.status = 'resolved';
                alert.resolved = true;
            }
        });
        
        document.querySelectorAll('.professional-alert-item.active').forEach(element => {
            element.classList.remove('active');
            element.classList.add('resolved');
        });
        
        this.updateStatistics();
        this.saveToStorage();
    }

    exportAlerts() {
        // Use backend export endpoint
        window.open('/api/fire-alerts/export/', '_blank');
        
        if (window.fireAlertIntegration && window.fireAlertIntegration.showToast) {
            window.fireAlertIntegration.showToast('Export started - check downloads', 'success');
        }
    }

    // Load alerts from backend
    async loadAlertsFromBackend() {
        try {
            const response = await fetch('/api/fire-alerts/?limit=50');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.alerts = data.alerts.map(alert => ({
                    id: alert.id,
                    camera_id: alert.camera_id,
                    farm_id: alert.farm_id,
                    confidence: alert.confidence,
                    timestamp: new Date(alert.timestamp),
                    status: alert.is_resolved ? 'resolved' : 'active',
                    priority: this.calculatePriority(alert.confidence),
                    resolved: alert.is_resolved,
                    notes: alert.notes || ''
                }));
                
                // Render alerts
                this.alerts.forEach(alert => this.renderAlert(alert));
                this.updateStatistics();
                this.updateBadge();
                
                console.log('✅ Loaded alerts from backend:', this.alerts.length);
            }
        } catch (error) {
            console.error('❌ Failed to load alerts from backend:', error);
            // Fallback to localStorage
            this.loadFromStorage();
        }
    }

    // Get CSRF token
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }

    testAlert() {
        const testAlert = {
            camera_id: `CAM-${Math.floor(Math.random() * 100)}`,
            farm_id: `FARM-${Math.floor(Math.random() * 10)}`,
            confidence: 0.85 + Math.random() * 0.15,
            timestamp: new Date().toISOString(),
            type: 'fire_detection'
        };
        
        this.addAlert(testAlert);
    }

    updateStatistics() {
        const total = this.alerts.length;
        const active = this.alerts.filter(a => a.status === 'active').length;
        const resolved = this.alerts.filter(a => a.status === 'resolved').length;
        
        const totalEl = document.getElementById('total-alerts');
        const activeEl = document.getElementById('active-alerts');
        const resolvedEl = document.getElementById('resolved-alerts');
        
        if (totalEl) totalEl.textContent = total;
        if (activeEl) activeEl.textContent = active;
        if (resolvedEl) resolvedEl.textContent = resolved;
    }

    updateBadge() {
        const badge = document.getElementById('alert-badge');
        const activeAlerts = this.alerts.filter(a => a.status === 'active').length;
        
        if (badge) {
            if (activeAlerts > 0) {
                badge.textContent = activeAlerts;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    toggleAlertPanel() {
        const panel = document.getElementById('alert-panel');
        if (panel) {
            panel.classList.toggle('show');
        }
    }

    hideAlertPanel() {
        const panel = document.getElementById('alert-panel');
        if (panel) {
            panel.classList.remove('show');
        }
    }

    checkIfNoAlerts() {
        const alertsList = document.getElementById('professional-alerts-list');
        const noAlertsMsg = document.getElementById('no-alerts-professional');
        
        if (alertsList && noAlertsMsg) {
            const hasAlerts = alertsList.querySelectorAll('.professional-alert-item').length > 0;
            noAlertsMsg.style.display = hasAlerts ? 'none' : 'block';
        }
    }

    playAlertSound() {
        if (!this.soundEnabled) return;
        
        // Create audio context for alert sound
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 0.2);
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        } catch (error) {
            console.warn('Could not play alert sound:', error);
        }
    }

    showBrowserNotification(alert) {
        if (this.notificationPermission === 'granted') {
            new Notification('🔥 Fire Alert!', {
                body: `Fire detected at Camera ${alert.camera_id}, Farm ${alert.farm_id}`,
                icon: '/static/geo/icons/fire.png',
                badge: '/static/geo/icons/fire-badge.png',
                tag: 'fire-alert',
                requireInteraction: true
            });
        }
    }

    toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        const btn = document.getElementById('sound-toggle-btn');
        const icon = btn?.querySelector('i');
        
        if (icon) {
            if (this.soundEnabled) {
                icon.className = 'fas fa-volume-up';
                btn.title = 'Disable Alert Sounds';
            } else {
                icon.className = 'fas fa-volume-mute';
                btn.title = 'Enable Alert Sounds';
            }
        }
        
        this.saveSettings();
    }

    updateConnectionStatus(status, message) {
        const indicator = document.getElementById('connection-status-indicator');
        const dot = indicator?.querySelector('.status-dot');
        const text = indicator?.querySelector('.status-text');
        
        if (dot && text) {
            dot.className = `status-dot ${status}`;
            text.textContent = message;
        }
    }

    applyFilters() {
        // Implementation for filtering alerts
        const statusFilter = document.getElementById('status-filter')?.value || 'all';
        const priorityFilter = document.getElementById('priority-filter')?.value || 'all';
        const timeFilter = document.getElementById('time-filter')?.value || 'all';
        
        document.querySelectorAll('.professional-alert-item').forEach(item => {
            let show = true;
            
            // Apply filters logic here
            if (statusFilter !== 'all') {
                show = show && item.classList.contains(statusFilter);
            }
            
            item.style.display = show ? 'block' : 'none';
        });
    }

    saveToStorage() {
        localStorage.setItem('fire_alerts', JSON.stringify(this.alerts));
    }

    loadFromStorage() {
        const stored = localStorage.getItem('fire_alerts');
        if (stored) {
            this.alerts = JSON.parse(stored);
            this.alerts.forEach(alert => this.renderAlert(alert));
            this.updateStatistics();
            this.updateBadge();
        }
    }

    saveSettings() {
        const settings = {
            soundEnabled: this.soundEnabled,
            filterSettings: this.filterSettings
        };
        localStorage.setItem('alert_manager_settings', JSON.stringify(settings));
    }

    loadSettings() {
        const stored = localStorage.getItem('alert_manager_settings');
        if (stored) {
            const settings = JSON.parse(stored);
            this.soundEnabled = settings.soundEnabled !== undefined ? settings.soundEnabled : true;
            this.filterSettings = { ...this.filterSettings, ...settings.filterSettings };
        }
        
        // Load alerts from backend instead of localStorage
        this.loadAlertsFromBackend();
    }

    initializeStatusIndicator() {
        this.updateConnectionStatus('connecting', 'Connecting to alert system...');
        
        // Auto-hide after 5 seconds if no status update
        setTimeout(() => {
            const indicator = document.getElementById('connection-status-indicator');
            if (indicator && !indicator.classList.contains('connected')) {
                indicator.style.opacity = '0.5';
            }
        }, 5000);
    }
}

// Initialize the professional alert manager
const alertManager = new AlertManager();

// Export for global access
window.alertManager = alertManager;
