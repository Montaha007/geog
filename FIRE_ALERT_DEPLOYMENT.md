# Fire Alert System - Production Deployment Guide

## 🔥 Smart For Green Fire Detection System

### System Overview
Your fire detection system consists of:
1. **Python Fire Detection Service** - YOLO-based fire detection with Redis publishing
2. **Django Backend** - Camera management and alert endpoints  
3. **WebSocket Notification Service** - Real-time communication bridge
4. **Frontend JavaScript** - Professional alert management UI

### ✅ Deployment Checklist

#### 1. Prerequisites
- [ ] Redis server running on port 6379
- [ ] Django server with Celery configured
- [ ] Node.js for WebSocket service (optional - can use Python)

#### 2. Backend Services
- [ ] Start Redis: `redis-server`
- [ ] Start Django: `python manage.py runserver`
- [ ] Start Notification Service: `python notification_service/notification.py`

#### 3. Frontend Integration
- [ ] Fire alerts CSS included in templates ✅
- [ ] Fire alerts JS included in templates ✅ 
- [ ] Socket.io library loaded ✅
- [ ] Alert dashboard div present ✅
- [ ] Professional Alert Manager CSS included ✅
- [ ] Professional Alert Manager JS included ✅
- [ ] Alert Manager integration bridge loaded ✅

#### 4. Professional Alert Manager Files
- [ ] `/static/geo/css/alert_manager.css` ✅
- [ ] `/static/geo/js/alert_manager.js` ✅ 
- [ ] `/static/geo/js/fire_alerts_integration.js` ✅
- [ ] Alert Manager documentation available ✅

#### 5. Backend API Endpoints
- [ ] Fire alert webhook endpoint: `/api/fire-alerts/webhook/` ✅
- [ ] Get alerts API: `/api/fire-alerts/` ✅
- [ ] Resolve alert API: `/api/fire-alerts/<id>/resolve/` ✅
- [ ] Delete alert API: `/api/fire-alerts/<id>/delete/` ✅
- [ ] Bulk resolve API: `/api/fire-alerts/bulk-resolve/` ✅
- [ ] Export alerts API: `/api/fire-alerts/export/` ✅
- [ ] Fire alerts dashboard: `/fire-alerts/dashboard/` ✅
- [ ] Alert demo page: `/demo/alerts/` ✅

#### 6. Database Models
- [ ] FireDetection model in cams app ✅
- [ ] Database migrations applied ✅

### 🎮 Demo & Testing

#### Alert Manager Demo Page
A comprehensive demo page is available at `/templates/Gis/alert_demo.html` featuring:
- **Interactive Controls**: Generate test alerts, open/close panels, test sounds
- **Feature Showcase**: Live demonstration of all alert manager capabilities  
- **Status Display**: Real-time counters and analytics
- **Keyboard Shortcuts Guide**: Complete list of available shortcuts
- **Feature Grid**: Visual overview of all system capabilities

#### Testing Features
- **Test Alert Generation**: Single and multiple alert generation
- **Sound Testing**: Audio notification testing
- **Browser Notification Testing**: Native OS notification testing
- **Export Testing**: Alert data export functionality
- **Panel Control Testing**: Show/hide panel operations

### � Mobile & Responsive Features

#### Mobile Optimization
- **Full-Screen Panel**: 100% width alert panel on mobile devices
- **Touch-Friendly Interface**: Large touch targets and gesture support
- **Responsive Statistics**: Adaptive layout for statistics display
- **Mobile Notifications**: Native mobile notification support

#### Responsive Breakpoints
- **Desktop (≥768px)**: 400px sliding panel from right
- **Tablet (768px-1024px)**: Adjusted panel width and spacing
- **Mobile (<768px)**: Full-screen overlay panel with optimized controls

### 🔧 Advanced Configuration

#### Customization Options
```javascript
// Alert Manager Configuration
const alertManager = new AlertManager({
    maxAlerts: 100,                    // Maximum alerts in memory
    autoResolveAfter: 3600000,        // Auto-resolve after 1 hour
    soundEnabled: true,                // Enable alert sounds
    notificationPermission: 'auto',    // Auto-request notification permission
    exportFormat: 'json',             // Default export format
    theme: 'auto'                      // Auto-detect dark/light mode
});

// Custom Priority Thresholds
alertManager.priorityThresholds = {
    high: 0.9,      // 90%+ confidence = High priority
    medium: 0.7,    // 70-89% confidence = Medium priority
    low: 0.0        // <70% confidence = Low priority
};
```

#### WebSocket Configuration
```javascript
// Enhanced WebSocket Settings
const socket = io("ws://localhost:5001", {
    transports: ["websocket"],
    reconnectionAttempts: 5,
    timeout: 10000,
    heartbeatInterval: 30000
});
```

### 📊 Analytics & Monitoring

#### Built-in Analytics
```javascript
// Access real-time analytics
const analytics = window.fireAlertAnalytics;
console.log({
    alertsReceived: analytics.alertsReceived,
    alertsResolved: analytics.alertsResolved,
    averageResponseTime: analytics.averageResponseTime,
    sessionStart: analytics.sessionStart
});
```

#### Performance Metrics
- **Memory Usage**: Automatic cleanup and optimization
- **Response Times**: Alert processing and display metrics
- **Connection Quality**: WebSocket connection stability monitoring
- **User Interaction**: Click-through rates and usage patterns

### 🚀 Deployment Steps

#### 1. Database Setup
```bash
# Apply migrations for FireDetection model
python manage.py makemigrations cams
python manage.py migrate
```

#### 2. Backend Services
```bash
# Start Redis (required for WebSocket)
redis-server

# Start Django development server
python manage.py runserver

# Start notification service (optional)
cd notification_service
python notification.py
```

#### 3. Test the System
```bash
# Test the webhook endpoint
python test_fire_alerts.py

# Or manually test with curl
curl -X POST http://localhost:8000/api/fire-alerts/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": "CAM-001", 
    "farm_id": "FARM-A", 
    "confidence": 0.92,
    "timestamp": "2025-01-29T10:30:00Z"
  }'
```

#### 4. Access the System
- **Main Dashboard**: http://localhost:8000/
- **Fire Alerts Dashboard**: http://localhost:8000/fire-alerts/dashboard/
- **Alert Demo**: http://localhost:8000/demo/alerts/
- **Interactive Map**: http://localhost:8000/ (default)

#### Professional Alert Manager UI
- **Alert Manager Button**: Red gradient button in top-right corner with animated badge
- **Sliding Alert Panel**: Professional 400px sliding panel from right side
- **Real-time Statistics**: Live counters for total, active, and resolved alerts
- **Advanced Filtering**: Filter by status, priority, and time range
- **Priority Classification**: Automatic High/Medium/Low priority based on confidence
- **Export Functionality**: Download alert data as JSON format
- **Sound Controls**: Toggle alert sounds on/off with speaker icon
- **Keyboard Shortcuts**: Quick access via Ctrl+Shift+A, Ctrl+Shift+T, Escape

#### Legacy Dashboard Integration
- **Status Bar**: Real-time connection status (bottom left)
- **Alert Manager**: Professional alert button (top right)
- **Alert Panel**: Slide-out panel with active alerts and history
- **Toast Notifications**: Non-intrusive notifications
- **Browser Notifications**: Native OS notifications

#### Alert Types
1. **Browser Notifications** - Native OS alerts with sound
2. **In-App Alerts** - Visual alerts within the application
3. **Toast Messages** - Status updates and confirmations
4. **Dashboard Integration** - Alerts display in your existing dashboard

#### Alert Management
- **Professional Alert Panel**: Modern sliding interface with 400px width
- **Active Alerts**: Current fire detections requiring attention with priority indicators
- **Alert History**: Recent detection history with filtering capabilities
- **Resolve/Delete Functions**: Individual alert management with animations
- **Bulk Actions**: Resolve all alerts or export data functionality
- **Auto-cleanup**: Old alerts automatically archived after 100 alerts limit
- **Analytics Tracking**: Real-time performance metrics and session statistics

#### Enhanced Integration Features
- **Dual Dashboard Support**: Works with both legacy and professional interfaces
- **Bridge Integration**: Seamless connection between old and new systems
- **Toast Notifications**: Modern non-intrusive status updates
- **Connection Monitoring**: Real-time WebSocket status with visual indicators
- **Keyboard Navigation**: Full keyboard shortcut support for power users
- **Responsive Design**: Mobile-optimized with full-screen panel on small devices
- **Dark Mode Support**: Automatic theme detection and custom color schemes

### 🔧 Configuration

#### Development Mode
- Test buttons available on localhost/127.0.0.1
- Debug logging enabled
- Message tracking active

#### Production Mode  
- Clean professional interface
- No test buttons
- Optimized performance
- Error handling

### 📱 Mobile Responsive
- Adapts to mobile screens
- Touch-friendly interface
- Responsive alert panels

### 🔐 Security Notes
- CSRF tokens included in Django requests
- CORS configured for WebSocket service
- No sensitive data in frontend JavaScript

### 🎨 Smart For Green Theme Integration
- Green color scheme for system status
- Professional alert styling
- Consistent with existing UI
- Smooth animations and transitions

### 📊 Monitoring
The system provides real-time feedback on:
- WebSocket connection status
- Alert count and management
- Service health indicators
- Message activity tracking

### 🔄 Testing the System

1. **Client Test**: Use the alert manager to verify frontend functionality
2. **Server Test**: Verify Django → Redis → WebSocket → Frontend pipeline  
3. **Real Alerts**: System automatically processes fire detection events

### 📞 Support
- Check browser console for detailed logging
- Monitor Django and Redis logs for backend issues
- WebSocket service logs show real-time activity

---

**Status**: ✅ Ready for Production
**Last Updated**: July 26, 2025
**Version**: 1.0.0
