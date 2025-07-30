// Replace with your backend notification service URL
const socket = io("http://localhost:5001", {
  transports: ["websocket"], // Enforce websocket transport for better compatibility
  reconnectionAttempts: 5,    // Optional: Retry connection attempts
  timeout: 10000              // Optional: Timeout for each connection attempt (in ms)
});

// Global variables for alert management
let alertCount = 0;
let alertHistory = [];

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  initializeAlertDashboard();
});

function initializeAlertDashboard() {
  // Add event listeners for dashboard controls
  const clearBtn = document.getElementById('clear-alerts-btn');
  const testBtn = document.getElementById('test-alert-btn');
  
  if (clearBtn) {
    clearBtn.addEventListener('click', clearAllAlerts);
  }
  
  if (testBtn) {
    testBtn.addEventListener('click', testFireAlert);
  }
}

// Function to add alert to dashboard
function addAlertToDashboard(alertData) {
  const alertsContainer = document.getElementById('alerts-container');
  const noAlertsMessage = document.getElementById('no-alerts-message');
  const alertCounter = document.getElementById('alert-counter');
  const clearBtn = document.getElementById('clear-alerts-btn');
  
  if (!alertsContainer) return;
  
  // Hide "no alerts" message
  if (noAlertsMessage) {
    noAlertsMessage.style.display = 'none';
  }
  
  // Create alert element
  const alertElement = document.createElement('div');
  alertElement.className = 'alert-item mb-2';
  alertElement.style.cssText = `
    background: white;
    border: 1px solid #dc3545;
    border-left: 4px solid #dc3545;
    border-radius: 6px;
    padding: 12px;
    animation: slideInDown 0.3s ease;
    box-shadow: 0 2px 4px rgba(220,53,69,0.1);
  `;
  
  const timestamp = new Date(alertData.timestamp || Date.now()).toLocaleString();
  const confidence = alertData.confidence ? `${(alertData.confidence * 100).toFixed(1)}%` : 'N/A';
  
  alertElement.innerHTML = `
    <div class="d-flex justify-content-between align-items-start">
      <div class="flex-grow-1">
        <div class="fw-bold text-danger mb-1">
          🔥 Fire Detected
        </div>
        <div class="small mb-1">
          <strong>Camera:</strong> ${alertData.camera_id || 'Unknown'} | 
          <strong>Farm:</strong> ${alertData.farm_id || 'Unknown'}
        </div>
        <div class="small mb-1">
          <strong>Confidence:</strong> ${confidence}
        </div>
        <div class="small text-muted">
          ${timestamp}
        </div>
      </div>
      <div class="ms-2">
        <button class="btn btn-sm btn-outline-danger" onclick="removeAlert(this)">
          ×
        </button>
      </div>
    </div>
  `;
  
  // Add to beginning of container
  alertsContainer.insertBefore(alertElement, alertsContainer.firstChild);
  
  // Update counter
  alertCount++;
  updateAlertCounter();
  
  // Show controls
  if (clearBtn) {
    clearBtn.style.display = 'inline-block';
  }
  
  // Store in history
  alertHistory.unshift({
    ...alertData,
    id: Date.now(),
    element: alertElement
  });
  
  // Limit to 10 alerts in dashboard
  if (alertHistory.length > 10) {
    const oldAlert = alertHistory.pop();
    if (oldAlert.element && oldAlert.element.parentNode) {
      oldAlert.element.remove();
    }
  }
}

// Update alert counter
function updateAlertCounter() {
  const alertCounter = document.getElementById('alert-counter');
  if (alertCounter) {
    if (alertCount > 0) {
      alertCounter.textContent = alertCount;
      alertCounter.style.display = 'inline-block';
      alertCounter.style.animation = 'pulse 1s infinite';
    } else {
      alertCounter.style.display = 'none';
    }
  }
}

// Remove individual alert
function removeAlert(button) {
  const alertElement = button.closest('.alert-item');
  if (alertElement) {
    alertElement.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => {
      alertElement.remove();
      alertCount = Math.max(0, alertCount - 1);
      updateAlertCounter();
      checkIfNoAlerts();
    }, 300);
  }
}

// Clear all alerts
function clearAllAlerts() {
  const alertsContainer = document.getElementById('alerts-container');
  const clearBtn = document.getElementById('clear-alerts-btn');
  
  if (alertsContainer) {
    // Remove all alert items
    const alertItems = alertsContainer.querySelectorAll('.alert-item');
    alertItems.forEach(item => item.remove());
    
    alertCount = 0;
    alertHistory = [];
    updateAlertCounter();
    
    if (clearBtn) {
      clearBtn.style.display = 'none';
    }
    
    checkIfNoAlerts();
  }
}

// Check if no alerts and show message
function checkIfNoAlerts() {
  const alertsContainer = document.getElementById('alerts-container');
  const noAlertsMessage = document.getElementById('no-alerts-message');
  
  if (alertsContainer && noAlertsMessage) {
    const hasAlerts = alertsContainer.querySelectorAll('.alert-item').length > 0;
    noAlertsMessage.style.display = hasAlerts ? 'none' : 'block';
  }
}

// Test fire alert function
function testFireAlert() {
  const testData = {
    camera_id: Math.floor(Math.random() * 10) + 1,
    farm_id: Math.floor(Math.random() * 5) + 1,
    confidence: 0.85 + Math.random() * 0.15, // 85-100%
    timestamp: new Date().toISOString(),
    type: 'fire_detection'
  };
  
  console.log('🧪 Testing fire alert with data:', testData);
  addAlertToDashboard(testData);
  
  // Also trigger other alert functions if they exist
  if (typeof showFireAlert === 'function') {
    showFireAlert(testData);
  }
}

// Connection event
socket.on("connect", () => {
  console.log("🔥 Connected to Fire Alert WebSocket");
  
  // Add connection indicator to dashboard
  const alertsContainer = document.getElementById('alerts-container');
  if (alertsContainer) {
    const connectionDiv = document.createElement('div');
    connectionDiv.id = 'connection-status';
    connectionDiv.className = 'alert alert-success alert-sm mb-2';
    connectionDiv.innerHTML = '🟢 Fire alert system connected';
    alertsContainer.insertBefore(connectionDiv, alertsContainer.firstChild);
    
    // Remove after 3 seconds
    setTimeout(() => {
      if (connectionDiv.parentNode) connectionDiv.remove();
    }, 3000);
  }
});

// Disconnection event
socket.on("disconnect", (reason) => {
  console.log("⛔ Fire Alert WebSocket disconnected:", reason);
  
  // Add disconnection indicator to dashboard
  const alertsContainer = document.getElementById('alerts-container');
  if (alertsContainer) {
    const disconnectionDiv = document.createElement('div');
    disconnectionDiv.className = 'alert alert-warning alert-sm mb-2';
    disconnectionDiv.innerHTML = '🟡 Fire alert system disconnected';
    alertsContainer.insertBefore(disconnectionDiv, alertsContainer.firstChild);
    
    // Remove after 5 seconds
    setTimeout(() => {
      if (disconnectionDiv.parentNode) disconnectionDiv.remove();
    }, 5000);
  }
});

// Error event
socket.on("connect_error", (error) => {
  console.error("❌ WebSocket connection error:", error);
  
  // Add error indicator to dashboard
  const alertsContainer = document.getElementById('alerts-container');
  if (alertsContainer) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-sm mb-2';
    errorDiv.innerHTML = '🔴 Fire alert system connection error';
    alertsContainer.insertBefore(errorDiv, alertsContainer.firstChild);
    
    // Remove after 5 seconds
    setTimeout(() => {
      if (errorDiv.parentNode) errorDiv.remove();
    }, 5000);
  }
});

// Custom event: fire_alert - Enhanced to work with dashboard
socket.on("fire_alert", (data) => {
  console.log("🚨 Fire Alert Received:", data);
  
  // Add to dashboard
  addAlertToDashboard(data);
  
  // OPTIONAL: Display it on the page (legacy support)
  if (document.getElementById("fire-alert-container")) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "fire-alert";
    alertDiv.innerHTML = `
      <h4>🔥 Fire Alert Detected</h4>
      <p><strong>Camera ID:</strong> ${data.camera_id}</p>
      <p><strong>Farm ID:</strong> ${data.farm_id}</p>
      <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
      <p><strong>Time:</strong> ${data.timestamp}</p>
      <img src="${data.image_url}" alt="Detected Fire" style="max-width: 300px;" />
      <hr />
    `;
    document.getElementById("fire-alert-container").prepend(alertDiv);
  }
  
  // Show browser notification if permission granted
  if (Notification.permission === "granted") {
    new Notification("🔥 Fire Detected!", {
      body: `Camera ${data.camera_id} detected fire at Farm ${data.farm_id}`,
      icon: "/static/icons/fire.png"
    });
  }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInDown {
    from { transform: translateY(-10px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  
  @keyframes slideOutRight {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
  
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }
  
  .alerts-list {
    max-height: 300px;
    overflow-y: auto;
  }
  
  .alerts-list::-webkit-scrollbar {
    width: 6px;
  }
  
  .alerts-list::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  
  .alerts-list::-webkit-scrollbar-thumb {
    background: #dc3545;
    border-radius: 3px;
  }
  
  .alert-item:hover {
    background: #f8f9fa !important;
    transform: translateX(2px);
    transition: all 0.2s ease;
  }
`;
document.head.appendChild(style);
