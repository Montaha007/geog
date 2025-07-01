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
