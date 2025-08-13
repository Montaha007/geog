/**
 * Enhanced Fire Alerts Integration
 * Bridges the existing fire_alerts.js with the new professional alert manager
 */

// Enhanced socket integration with professional alert manager
(function() {
    'use strict';

    // Wait for alert manager to be initialized
    function waitForAlertManager(callback) {
        if (window.alertManager && window.alertManager.isInitialized) {
            callback();
        } else {
            setTimeout(() => waitForAlertManager(callback), 100);
        }
    }

    // Initialize enhanced integration
    waitForAlertManager(() => {
        console.log('🔗 Integrating professional alert manager with fire alerts system');
        
        // Override the existing socket events to work with professional alert manager
        if (typeof socket !== 'undefined') {
            initializeEnhancedSocketIntegration();
        }
        
        // Enhance existing dashboard functionality
        enhanceExistingDashboard();
        
        // Initialize toast notifications
        initializeToastNotifications();
        
        // Initialize keyboard shortcuts
        initializeKeyboardShortcuts();
    });

    function initializeEnhancedSocketIntegration() {
        // Enhanced connection handling
        socket.off('connect').on('connect', () => {
            console.log('🔥 Enhanced Fire Alert WebSocket connected');
            window.alertManager.updateConnectionStatus('connected', 'Fire alert system connected');
            showToast('Connected to fire alert system', 'success');
            
            // Legacy dashboard support
            updateLegacyConnectionStatus('connected');
        });

        // Enhanced disconnection handling
        socket.off('disconnect').on('disconnect', (reason) => {
            console.log('⛔ Enhanced Fire Alert WebSocket disconnected:', reason);
            window.alertManager.updateConnectionStatus('disconnected', 'Fire alert system disconnected');
            showToast('Disconnected from fire alert system', 'warning');
            
            // Legacy dashboard support
            updateLegacyConnectionStatus('disconnected');
        });

      

        // Enhanced fire alert handling
        socket.off('fire_alert').on('fire_alert', (data) => {
            console.log('🚨 Enhanced Fire Alert Received:', data);
            
            // Add to professional alert manager
            window.alertManager.addAlert(data);
            
            // Also update legacy dashboard for backward compatibility
            if (typeof addAlertToDashboard === 'function') {
                addAlertToDashboard(data);
            }
            
            // Show toast notification
            showToast(`Fire detected at Camera ${data.camera_id}`, 'error');
            
            // Legacy browser notification support
            if (Notification.permission === "granted") {
                new Notification("🔥 Fire Detected!", {
                    body: `Camera ${data.camera_id} detected fire at Farm ${data.farm_id}`,
                    icon: "/static/geo/icons/fire.png",
                    badge: "/static/geo/icons/fire-badge.png",
                    tag: 'fire-alert',
                    requireInteraction: true
                });
            }

            // Update legacy alert container if it exists
            updateLegacyAlertContainer(data);
        });

        // Add heartbeat monitoring
        let heartbeatInterval;
        socket.on('connect', () => {
            heartbeatInterval = setInterval(() => {
                socket.emit('heartbeat');
            }, 30000); // Send heartbeat every 30 seconds
        });

        socket.on('disconnect', () => {
            if (heartbeatInterval) {
                clearInterval(heartbeatInterval);
            }
        });
    }

    function enhanceExistingDashboard() {
        // Enhance the existing alert dashboard
        const existingDashboard = document.getElementById('alerts-dashboard');
        if (existingDashboard) {
            // Add professional styling
            existingDashboard.classList.add('enhanced-alert-dashboard');
            
            // Add integration buttons
            addIntegrationControls(existingDashboard);
        }

        // Enhance existing test button
        const existingTestBtn = document.getElementById('test-alert-btn');
        if (existingTestBtn) {
            existingTestBtn.addEventListener('click', () => {
                // Also trigger professional alert manager test
                if (window.alertManager) {
                    window.alertManager.testAlert();
                }
            });
        }

        // Enhance existing clear button
        const existingClearBtn = document.getElementById('clear-alerts-btn');
        if (existingClearBtn) {
            existingClearBtn.addEventListener('click', () => {
                // Also clear professional alert manager
                if (window.alertManager) {
                    window.alertManager.resolveAllAlerts();
                }
            });
        }
    }

    function addIntegrationControls(dashboard) {
        const integrationControls = document.createElement('div');
        integrationControls.className = 'integration-controls mt-3 pt-3 border-top';
        integrationControls.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">Professional Alert Manager</small>
                <button id="open-professional-manager" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt"></i> Open Manager
                </button>
            </div>
        `;
        
        dashboard.appendChild(integrationControls);
        
        // Add event listener
        const openBtn = document.getElementById('open-professional-manager');
        if (openBtn) {
            openBtn.addEventListener('click', () => {
                if (window.alertManager) {
                    window.alertManager.toggleAlertPanel();
                }
            });
        }
    }

    function updateLegacyConnectionStatus(status) {
        const alertsContainer = document.getElementById('alerts-container');
        if (!alertsContainer) return;

        // Remove existing status indicators
        const existingStatus = alertsContainer.querySelectorAll('.connection-status-legacy');
        existingStatus.forEach(el => el.remove());

        // Add new status indicator
        const statusDiv = document.createElement('div');
        statusDiv.className = 'connection-status-legacy alert alert-sm mb-2';
        
        switch (status) {
            case 'connected':
                statusDiv.classList.add('alert-success');
                statusDiv.innerHTML = '🟢 Enhanced fire alert system connected';
                break;
            case 'disconnected':
                statusDiv.classList.add('alert-warning');
                statusDiv.innerHTML = '🟡 Enhanced fire alert system disconnected';
                break;
            case 'error':
                statusDiv.classList.add('alert-danger');
                statusDiv.innerHTML = '🔴 Enhanced fire alert system connection error';
                break;
        }
        
        alertsContainer.insertBefore(statusDiv, alertsContainer.firstChild);
        
        // Auto-remove after delay
        setTimeout(() => {
            if (statusDiv.parentNode) statusDiv.remove();
        }, status === 'connected' ? 3000 : 5000);
    }

    function updateLegacyAlertContainer(data) {
        const legacyContainer = document.getElementById("fire-alert-container");
        if (legacyContainer) {
            const alertDiv = document.createElement("div");
            alertDiv.className = "fire-alert enhanced-legacy-alert";
            alertDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h5>🔥 Fire Alert Detected</h5>
                    <div class="row">
                        <div class="col-6">
                            <strong>Camera ID:</strong> ${data.camera_id || 'Unknown'}
                        </div>
                        <div class="col-6">
                            <strong>Farm ID:</strong> ${data.farm_id || 'Unknown'}
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-6">
                            <strong>Confidence:</strong> ${((data.confidence || 0) * 100).toFixed(2)}%
                        </div>
                        <div class="col-6">
                            <strong>Time:</strong> ${new Date(data.timestamp).toLocaleString()}
                        </div>
                    </div>
                    ${data.image_url ? `<img src="${data.image_url}" alt="Detected Fire" class="img-fluid mt-2" style="max-width: 100%; border-radius: 8px;" />` : ''}
                    <div class="mt-3">
                        <button class="btn btn-sm btn-outline-primary me-2" onclick="window.alertManager?.toggleAlertPanel()">
                            Open Alert Manager
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="this.closest('.enhanced-legacy-alert').remove()">
                            Dismiss
                        </button>
                    </div>
                </div>
                <hr />
            `;
            legacyContainer.prepend(alertDiv);
        }
    }

    // Toast notification system
    let toastContainer;

    function initializeToastNotifications() {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 440px;
            z-index: 1100;
            max-width: 350px;
        `;
        document.body.appendChild(toastContainer);
    }

    function showToast(message, type = 'info', duration = 5000) {
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast-notification ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-triangle',
            warning: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle'
        };

        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };

        toast.innerHTML = `
            <div class="d-flex align-items-start">
                <i class="${icons[type]}" style="color: ${colors[type]}; margin-right: 10px; margin-top: 2px;"></i>
                <div class="flex-grow-1">
                    <div class="toast-message">${message}</div>
                </div>
                <button class="btn btn-sm btn-link p-0 ms-2" onclick="this.closest('.toast-notification').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        toastContainer.appendChild(toast);

        // Auto-remove after duration
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, duration);
    }

    // Keyboard shortcuts
    function initializeKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Shift + A: Toggle alert panel
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'A') {
                e.preventDefault();
                if (window.alertManager) {
                    window.alertManager.toggleAlertPanel();
                }
            }

            // Ctrl/Cmd + Shift + T: Test alert
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                if (window.alertManager) {
                    window.alertManager.testAlert();
                }
            }

            // Escape: Close alert panel
            if (e.key === 'Escape') {
                if (window.alertManager) {
                    window.alertManager.hideAlertPanel();
                }
            }
        });
    }

    // Enhanced analytics and reporting
    function initializeAnalytics() {
        const analytics = {
            alertsReceived: 0,
            alertsResolved: 0,
            averageResponseTime: 0,
            lastAlert: null,
            sessionStart: new Date()
        };

        // Track alert metrics
        if (window.alertManager) {
            const originalAddAlert = window.alertManager.addAlert.bind(window.alertManager);
            window.alertManager.addAlert = function(alertData) {
                analytics.alertsReceived++;
                analytics.lastAlert = new Date();
                
                // Call original method
                originalAddAlert(alertData);
                
                // Update analytics dashboard if exists
                updateAnalyticsDashboard(analytics);
            };

            const originalResolveAlert = window.alertManager.resolveAlert.bind(window.alertManager);
            window.alertManager.resolveAlert = function(alertId) {
                analytics.alertsResolved++;
                
                // Call original method
                originalResolveAlert(alertId);
                
                // Update analytics dashboard if exists
                updateAnalyticsDashboard(analytics);
            };
        }

        // Expose analytics globally
        window.fireAlertAnalytics = analytics;
    }

    function updateAnalyticsDashboard(analytics) {
        // This could be extended to show real-time analytics
        console.log('📊 Fire Alert Analytics:', analytics);
    }

    // Initialize analytics
    initializeAnalytics();

    // Expose helper functions globally
    window.fireAlertIntegration = {
        showToast,
        updateLegacyConnectionStatus,
        updateLegacyAlertContainer
    };

    console.log('✅ Enhanced fire alerts integration initialized');
})();
