class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.mainContent = document.getElementById('mainContent');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.mobileMenuBtn = document.getElementById('mobileMenuBtn');
        this.mobileOverlay = document.getElementById('mobileOverlay');
        this.isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        this.isMobileOpen = false;

        this.init();
    }

    init() {
        // Set initial state
        if (this.isCollapsed && window.innerWidth >= 768) {
            this.collapse();
        } else {
            this.expand();
        }

        // Set active nav link
        this.setActiveNavLink();

        // Event listeners
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', () => this.toggle());
        }
        if (this.mobileMenuBtn) {
            this.mobileMenuBtn.addEventListener('click', () => this.toggleMobile());
        }
        if (this.mobileOverlay) {
            this.mobileOverlay.addEventListener('click', () => this.closeMobile());
        }

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) {
                this.closeMobile();
            }
        });
    }

    toggle() {
        this.isCollapsed = !this.isCollapsed;
        localStorage.setItem('sidebarCollapsed', this.isCollapsed);

        if (this.isCollapsed) {
            this.collapse();
        } else {
            this.expand();
        }
    }

    collapse() {
        this.sidebar.classList.add('collapsed');
        this.mainContent.classList.add('expanded');
        if (this.sidebarToggle) {
            this.sidebarToggle.innerHTML = '<i class="fas fa-chevron-right"></i>';
        }
    }

    expand() {
        this.sidebar.classList.remove('collapsed');
        this.mainContent.classList.remove('expanded');
        if (this.sidebarToggle) {
            this.sidebarToggle.innerHTML = '<i class="fas fa-chevron-left"></i>';
        }
    }

    toggleMobile() {
        this.isMobileOpen = !this.isMobileOpen;

        if (this.isMobileOpen) {
            this.openMobile();
        } else {
            this.closeMobile();
        }
    }

    openMobile() {
        this.sidebar.classList.add('mobile-open');
        if (this.mobileOverlay) {
            this.mobileOverlay.classList.add('show');
        }
        document.body.style.overflow = 'hidden';
    }

    closeMobile() {
        this.sidebar.classList.remove('mobile-open');
        if (this.mobileOverlay) {
            this.mobileOverlay.classList.remove('show');
        }
        document.body.style.overflow = '';
        this.isMobileOpen = false;
    }

    setActiveNavLink() {
        const navLinks = this.sidebar.querySelectorAll('.nav-link');
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }
}

// Initialize SidebarManager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new SidebarManager();
});
// ...existing code...
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.isOpen = false;
        this.init();
    }

    init() {
        this.notificationBtn = document.getElementById('notificationBtn');
        this.notificationPopup = document.getElementById('notificationPopup');
        this.notificationBadge = document.getElementById('notificationBadge');
        this.notificationList = document.getElementById('notificationList');
        this.clearBtn = document.querySelector('.clear-notifications');

        this.bindEvents();
        this.loadStoredNotifications();
        this.updateBadge();
    }

    bindEvents() {
        // Toggle notification popup
        this.notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.togglePopup();
        });

        // Clear all notifications
        this.clearBtn.addEventListener('click', () => {
            this.clearAllNotifications();
        });

        // Close popup when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.notificationPopup.contains(e.target) && !this.notificationBtn.contains(e.target)) {
                this.closePopup();
            }
        });

        // Prevent popup from closing when clicking inside
        this.notificationPopup.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    togglePopup() {
        if (this.isOpen) {
            this.closePopup();
        } else {
            this.openPopup();
        }
    }

    openPopup() {
        this.notificationPopup.classList.add('show');
        this.isOpen = true;
    }

    closePopup() {
        this.notificationPopup.classList.remove('show');
        this.isOpen = false;
    }

    addNotification(data) {
        const notification = {
            id: Date.now() + Math.random(),
            title: data.title || 'New Location',
            description: data.description || 'Location saved successfully',
            time: new Date().toLocaleString(),
            icon: data.icon || 'fas fa-map-marker-alt',
            ...data
        };

        this.notifications.unshift(notification);
        
        // Keep only the last 50 notifications
        if (this.notifications.length > 50) {
            this.notifications = this.notifications.slice(0, 50);
        }

        this.updateBadge();
        this.renderNotifications();
        this.saveNotifications();
        this.showBadgeAnimation();
    }

    removeNotification(id) {
        this.notifications = this.notifications.filter(n => n.id !== id);
        this.updateBadge();
        this.renderNotifications();
        this.saveNotifications();
    }

    clearAllNotifications() {
        this.notifications = [];
        this.updateBadge();
        this.renderNotifications();
        this.saveNotifications();
    }

    updateBadge() {
        const count = this.notifications.length;
        this.notificationBadge.textContent = count;
        this.notificationBadge.setAttribute('data-count', count);
        
        if (count === 0) {
            this.notificationBadge.style.display = 'none';
        } else {
            this.notificationBadge.style.display = 'flex';
        }
    }

    showBadgeAnimation() {
        this.notificationBadge.style.animation = 'none';
        setTimeout(() => {
            this.notificationBadge.style.animation = 'pulse 2s infinite';
        }, 10);
    }

    renderNotifications() {
        if (this.notifications.length === 0) {
            this.notificationList.innerHTML = `
                <div class="notification-empty">
                    <i class="fas fa-map-marker-alt"></i>
                    <p>No locations saved yet</p>
                </div>
            `;
            return;
        }

        this.notificationList.innerHTML = this.notifications.map(notification => `
            <div class="notification-item" data-id="${notification.id}">
                <div class="notification-icon">
                    <i class="${notification.icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${this.escapeHtml(notification.title)}</div>
                    <div class="notification-description">${this.escapeHtml(notification.description)}</div>
                    <div class="notification-time">${notification.time}</div>
                </div>
            </div>
        `).join('');

        // Add click events to notifications
        this.notificationList.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = parseInt(e.currentTarget.dataset.id);
                this.handleNotificationClick(id);
            });
        });
    }

    handleNotificationClick(id) {
        const notification = this.notifications.find(n => n.id === id);
        if (notification && notification.onClick) {
            notification.onClick(notification);
        }
        this.closePopup();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    saveNotifications() {
        try {
            localStorage.setItem('smartForGreenNotifications', JSON.stringify(this.notifications));
        } catch (e) {
            console.warn('Could not save notifications to localStorage:', e);
        }
    }

    loadStoredNotifications() {
        try {
            const stored = localStorage.getItem('smartForGreenNotifications');
            if (stored) {
                this.notifications = JSON.parse(stored);
                this.renderNotifications();
            }
        } catch (e) {
            console.warn('Could not load notifications from localStorage:', e);
            this.notifications = [];
        }
    }

    // Utility method to format time
    formatTime(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;
        return date.toLocaleDateString();
    }

    // Public method to add location notification
    addLocationNotification(location) {
        this.addNotification({
            title: 'Location Saved',
            description: `${location.name || 'New location'} has been saved to your map`,
            icon: 'fas fa-map-marker-alt',
            onClick: (notification) => {
                // Navigate to map or specific location
                if (typeof window.showLocationOnMap === 'function') {
                    window.showLocationOnMap(location);
                }
            }
        });
    }

    // Public method to add drawing notification
    addDrawingNotification(shape) {
        this.addNotification({
            title: `${shape.type} Created`,
            description: `New ${shape.type.toLowerCase()} has been drawn on the map`,
            icon: 'fas fa-pencil-alt',
            onClick: (notification) => {
                // Navigate to the drawn shape
                if (typeof window.focusOnShape === 'function') {
                    window.focusOnShape(shape);
                }
            }
        });
    }

    // Public method to add general notification
    addGeneralNotification(title, description, icon = 'fas fa-info-circle') {
        this.addNotification({
            title: title,
            description: description,
            icon: icon
        });
    }
}

// Initialize notification system when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.notificationSystem = new NotificationSystem();
    
    // Example usage - you can call these from your other scripts
    window.addLocationNotification = (location) => {
        window.notificationSystem.addLocationNotification(location);
    };
    
    window.addDrawingNotification = (shape) => {
        window.notificationSystem.addDrawingNotification(shape);
    };
    
    window.addGeneralNotification = (title, description, icon) => {
        window.notificationSystem.addGeneralNotification(title, description, icon);
    };
});
