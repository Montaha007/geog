# Professional Alert Management System - Documentation

## 🚀 Overview

The Professional Alert Management System is a comprehensive fire detection alert interface for the Smart For Green platform. It provides real-time monitoring, professional UI components, and advanced alert management capabilities.

## ✨ Features

### Core Features
- **Real-time Fire Alerts**: Instant notifications when fire is detected
- **Professional Sliding Panel**: Modern, responsive alert management interface
- **Priority-based Alerts**: High, Medium, Low priority classification
- **Alert Statistics**: Real-time counters and analytics
- **Sound Notifications**: Configurable audio alerts
- **Browser Notifications**: Native OS notifications
- **Toast Messages**: Non-intrusive status updates
- **Connection Status**: Real-time WebSocket connection monitoring

### Advanced Features
- **Alert Filtering**: Filter by status, priority, and time range
- **Export Functionality**: Download alerts as JSON
- **Keyboard Shortcuts**: Quick access via keyboard
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode Support**: Automatic dark mode detection
- **Analytics Tracking**: Performance metrics and reporting
- **Legacy Integration**: Works with existing alert dashboard

## 🎯 User Interface Components

### 1. Alert Manager Button
- **Location**: Top-right corner of the page
- **Features**: 
  - Red gradient design with fire icon
  - Animated badge showing active alert count
  - Hover effects and smooth transitions

### 2. Professional Alert Panel
- **Type**: Sliding panel from right side
- **Sections**:
  - Header with statistics
  - Filter controls
  - Alert list with scrolling
  - Action buttons

### 3. Connection Status Indicator
- **Location**: Bottom-left corner
- **States**:
  - 🟢 Connected (Green)
  - 🟡 Connecting (Yellow) 
  - 🔴 Disconnected (Red)
  - 🟠 Error (Orange)

### 4. Toast Notifications
- **Location**: Top-right (next to alert panel)
- **Types**: Success, Error, Warning, Info
- **Auto-dismiss**: Configurable duration

## 🔧 Technical Implementation

### File Structure
```
geo/static/geo/
├── css/
│   ├── alert_manager.css          # Professional UI styles
│   └── fire_alerts.css            # Legacy alert styles
└── js/
    ├── alert_manager.js           # Core alert manager
    ├── fire_alerts.js             # Legacy alert system
    └── fire_alerts_integration.js # Integration bridge
```

### Key Classes

#### AlertManager
Main class handling professional alert management:

```javascript
class AlertManager {
    constructor()               // Initialize the system
    addAlert(alertData)         // Add new fire alert
    resolveAlert(alertId)       // Mark alert as resolved
    deleteAlert(alertId)        // Remove alert completely
    exportAlerts()              // Export alerts to JSON
    toggleAlertPanel()          // Show/hide alert panel
    updateConnectionStatus()    // Update connection indicator
}
```

### Integration Points

#### WebSocket Events
```javascript
socket.on('fire_alert', (data) => {
    // Received fire detection data
    alertManager.addAlert(data);
});

socket.on('connect', () => {
    // Connection established
    alertManager.updateConnectionStatus('connected', 'Connected');
});
```

#### Alert Data Structure
```javascript
{
    id: "unique_identifier",
    camera_id: "CAM-001",
    farm_id: "FARM-A",
    confidence: 0.92,
    timestamp: "2025-01-28T10:30:00Z",
    priority: "high",
    status: "active",
    resolved: false
}
```

## 🚀 Usage Guide

### For Users

#### Opening Alert Manager
1. Click the red "Alerts" button in the top-right corner
2. Or use keyboard shortcut: `Ctrl/Cmd + Shift + A`

#### Managing Alerts
1. **View Alerts**: Scroll through the alert list
2. **Filter Alerts**: Use dropdown filters for status, priority, time
3. **Resolve Alert**: Click the green checkmark button
4. **Delete Alert**: Click the red trash button
5. **Resolve All**: Click "Resolve All" button at bottom
6. **Export**: Click "Export" to download alert data

#### Sound Controls
- Click the speaker icon to toggle sound on/off
- Sound plays when new alerts arrive

#### Keyboard Shortcuts
- `Ctrl/Cmd + Shift + A`: Toggle alert panel
- `Ctrl/Cmd + Shift + T`: Test alert
- `Escape`: Close alert panel

### For Developers

#### Adding New Alert Types
```javascript
// Custom alert data
const customAlert = {
    camera_id: "CAM-005",
    farm_id: "FARM-B", 
    confidence: 0.88,
    type: "fire_detection",
    custom_data: {
        location: "Field 3",
        weather: "Dry"
    }
};

// Add to system
alertManager.addAlert(customAlert);
```

#### Extending Functionality
```javascript
// Add custom event listeners
alertManager.addEventListener('alertAdded', (alert) => {
    console.log('New alert added:', alert);
});

// Custom notification handler
alertManager.onAlertReceived = (alert) => {
    // Custom logic here
    sendToExternalSystem(alert);
};
```

## 🎨 Customization

### Themes
The system supports automatic dark mode detection and custom themes:

```css
/* Custom theme variables */
:root {
    --alert-primary-color: #dc3545;
    --alert-secondary-color: #6c757d;
    --alert-success-color: #28a745;
    --alert-warning-color: #ffc107;
}
```

### Priority Colors
```css
.high-priority { border-left-color: #dc3545; }    /* Red */
.medium-priority { border-left-color: #ffc107; }  /* Yellow */
.low-priority { border-left-color: #17a2b8; }     /* Blue */
```

## 📱 Responsive Design

The alert system is fully responsive:

- **Desktop**: Full-width panel (400px)
- **Tablet**: Adjusted panel width
- **Mobile**: Full-screen panel overlay

### Breakpoints
- `≥768px`: Desktop layout
- `<768px`: Mobile layout with full-screen panel

## 🔊 Audio Features

### Sound Configuration
```javascript
// Enable/disable sounds
alertManager.soundEnabled = true;

// Custom sound frequency
alertManager.playCustomSound(frequency, duration);
```

### Browser Notifications
Automatic permission request for native notifications:
```javascript
// Check permission status
console.log(alertManager.notificationPermission);

// Manual permission request
await alertManager.requestNotificationPermission();
```

## 📊 Analytics & Reporting

### Built-in Analytics
```javascript
// Access analytics data
const analytics = window.fireAlertAnalytics;
console.log({
    alertsReceived: analytics.alertsReceived,
    alertsResolved: analytics.alertsResolved,
    sessionStart: analytics.sessionStart
});
```

### Export Options
- **JSON**: Complete alert data
- **CSV**: Spreadsheet-compatible format
- **PDF**: Print-friendly reports (future feature)

## 🔒 Security Considerations

### Data Storage
- Alerts stored in browser localStorage
- No sensitive data transmitted
- Automatic cleanup of old alerts

### WebSocket Security
- Uses secure WebSocket connections (WSS) in production
- Authentication tokens supported
- Rate limiting on server side

## 🚀 Performance

### Optimization Features
- **Lazy Loading**: Alerts loaded on demand
- **Virtual Scrolling**: Handles thousands of alerts
- **Memory Management**: Automatic cleanup
- **Debounced Updates**: Prevents excessive re-renders

### Memory Usage
- Maximum 100 alerts in memory
- Automatic archiving of old alerts
- Efficient DOM manipulation

## 🛠️ Installation & Setup

### 1. File Inclusion
Add to your Django template:
```django
<!-- CSS -->
<link rel="stylesheet" href="{% static 'geo/css/alert_manager.css' %}">

<!-- JavaScript -->
<script src="{% static 'geo/js/alert_manager.js' %}"></script>
<script src="{% static 'geo/js/fire_alerts_integration.js' %}"></script>
```

### 2. WebSocket Configuration
Configure your WebSocket server URL:
```javascript
const socket = io("ws://your-server:5001");
```

### 3. Initialize
The system auto-initializes on page load:
```javascript
// Manual initialization if needed
const alertManager = new AlertManager();
```

## 🐛 Troubleshooting

### Common Issues

#### Alert Panel Not Showing
- Check console for JavaScript errors
- Verify CSS files are loaded
- Ensure AlertManager is initialized

#### WebSocket Not Connecting
- Verify server URL in fire_alerts.js
- Check network connectivity
- Review browser console for connection errors

#### No Sound Notifications
- Check browser sound permissions
- Verify soundEnabled setting
- Test with system sound enabled

### Debug Mode
Enable debug logging:
```javascript
// Enable debug mode
alertManager.debugMode = true;

// Check system status
console.log(alertManager.getSystemStatus());
```

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time collaboration (multi-user alerts)
- [ ] Custom alert rules and triggers
- [ ] Integration with external monitoring systems
- [ ] Mobile app companion
- [ ] Advanced analytics dashboard
- [ ] Automated incident response
- [ ] Machine learning alert prioritization

### API Extensions
- RESTful API for alert management
- Webhook integration for external systems
- Real-time metrics API
- Alert history API with pagination

## 📞 Support

For technical support or feature requests:

1. **Documentation**: Check this comprehensive guide
2. **Code Examples**: Review the JavaScript files
3. **Console Debugging**: Use browser developer tools
4. **Server Logs**: Check WebSocket server logs

### Development Resources
- **GitHub Repository**: [Your repo URL]
- **API Documentation**: [Your API docs URL]
- **Video Tutorials**: [Your tutorial URL]

---

*Smart For Green - Professional Fire Detection Alert Management System*
*Version 1.0 - January 2025*
