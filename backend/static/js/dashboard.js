const API_BASE = '/api';

class Dashboard {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.init();
    }

    init() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        this.loadUserInfo();
        this.loadDashboardData();
        this.loadRecentProjects();
        this.loadMyTasks();
        this.setupEventListeners();
    }

    async makeRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        };

        const response = await fetch(url, { ...defaultOptions, ...options });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/';
            return;
        }

        return response;
    }

    async loadUserInfo() {
        try {
            const response = await this.makeRequest(`${API_BASE}/core/profiles/me/`);
            if (response.ok) {
                const data = await response.json();
                document.getElementById('username').textContent = data.user.first_name || data.user.username;
            }
        } catch (error) {
            console.error('Failed to load user info:', error);
        }
    }

    async loadDashboardData() {
        try {
            const response = await this.makeRequest(`${API_BASE}/dashboard/widgets/dashboard_data/`);
            if (response.ok) {
                const data = await response.json();
                this.updateStatistics(data);
            }
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }

    updateStatistics(data) {
        document.getElementById('totalProjects').textContent = data.projects?.total || 0;
        document.getElementById('totalTasks').textContent = data.tasks?.total || 0;
        document.getElementById('completedTasks').textContent = data.tasks?.completed || 0;
        document.getElementById('overdueTasks').textContent = data.tasks?.overdue || 0;
    }

    async loadRecentProjects() {
        try {
            const response = await this.makeRequest(`${API_BASE}/dashboard/projects/?limit=5`);
            if (response.ok) {
                const data = await response.json();
                this.renderProjects(data.results || []);
            }
        } catch (error) {
            console.error('Failed to load projects:', error);
        }
    }

    renderProjects(projects) {
        const container = document.getElementById('recentProjects');

        if (projects.length === 0) {
            container.innerHTML = '<p class="empty-state">No projects yet. Create your first project!</p>';
            return;
        }

        container.innerHTML = projects.map(project => `
            <div class="project-item">
                <div class="project-color" style="background-color: ${project.color}"></div>
                <div class="project-info">
                    <div class="project-name">${project.name}</div>
                    <div class="project-meta">${project.tasks_count} tasks • Created ${this.formatDate(project.created_at)}</div>
                </div>
            </div>
        `).join('');
    }

    async loadMyTasks() {
        try {
            const response = await this.makeRequest(`${API_BASE}/dashboard/tasks/my_tasks/?limit=5`);
            if (response.ok) {
                const data = await response.json();
                this.renderTasks(data);
            }
        } catch (error) {
            console.error('Failed to load tasks:', error);
        }
    }

    renderTasks(tasks) {
        const container = document.getElementById('myTasks');

        if (tasks.length === 0) {
            container.innerHTML = '<p class="empty-state">No tasks assigned to you yet.</p>';
            return;
        }

        container.innerHTML = tasks.map(task => `
            <div class="task-item">
                <div class="task-info">
                    <div class="task-title">${task.title}</div>
                    <div class="task-meta">${task.project} • ${this.formatDate(task.created_at)}</div>
                </div>
                <div class="task-labels">
                    <span class="task-priority priority-${task.priority}">${task.priority}</span>
                    <span class="task-status status-${task.status.replace('_', '-')}">${this.formatStatus(task.status)}</span>
                </div>
            </div>
        `).join('');
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
        return date.toLocaleDateString();
    }

    formatStatus(status) {
        return status.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    setupEventListeners() {
        // Navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');

                // Here you would implement routing to different views
                const page = item.querySelector('span').textContent.toLowerCase();
                this.navigateToPage(page);
            });
        });

        // Search functionality
        const searchInput = document.querySelector('.search-bar input');
        searchInput.addEventListener('input', (e) => {
            this.performSearch(e.target.value);
        });

        // Notifications
        document.querySelector('.notifications').addEventListener('click', () => {
            this.toggleNotifications();
        });

        // User menu
        document.querySelector('.user-avatar').addEventListener('click', () => {
            this.toggleUserMenu();
        });

        // Auto-refresh data every 5 minutes
        setInterval(() => {
            this.loadDashboardData();
        }, 5 * 60 * 1000);
    }

    navigateToPage(page) {
        console.log(`Navigating to ${page}`);
        // Implement actual page routing here
        // For now, just show a notification
        this.showNotification(`${page} page - Coming soon!`, 'info');
    }

    performSearch(query) {
        if (query.length < 2) return;

        // Implement search functionality
        console.log(`Searching for: ${query}`);
    }

    toggleNotifications() {
        // Implement notifications dropdown
        this.showNotification('Notifications feature coming soon!', 'info');
    }

    toggleUserMenu() {
        // Implement user menu dropdown
        const menu = document.createElement('div');
        menu.className = 'user-dropdown';
        menu.innerHTML = `
            <div class="dropdown-item" onclick="dashboard.viewProfile()">
                <i class="fas fa-user"></i> Profile
            </div>
            <div class="dropdown-item" onclick="dashboard.viewSettings()">
                <i class="fas fa-cog"></i> Settings
            </div>
            <div class="dropdown-item" onclick="dashboard.logout()">
                <i class="fas fa-sign-out-alt"></i> Logout
            </div>
        `;

        // Remove existing dropdown
        document.querySelector('.user-dropdown')?.remove();

        // Add styles for dropdown
        const styles = `
            .user-dropdown {
                position: absolute;
                top: 60px;
                right: 20px;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                min-width: 180px;
                z-index: 1000;
            }
            .dropdown-item {
                display: flex;
                align-items: center;
                padding: 12px 16px;
                cursor: pointer;
                transition: background 0.2s;
            }
            .dropdown-item:hover {
                background: #f7fafc;
            }
            .dropdown-item i {
                margin-right: 8px;
                width: 16px;
            }
        `;

        if (!document.getElementById('dropdown-styles')) {
            const styleSheet = document.createElement('style');
            styleSheet.id = 'dropdown-styles';
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }

        document.body.appendChild(menu);

        // Close dropdown when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeDropdown(e) {
                if (!menu.contains(e.target) && !document.querySelector('.user-avatar').contains(e.target)) {
                    menu.remove();
                    document.removeEventListener('click', closeDropdown);
                }
            });
        }, 100);
    }

    viewProfile() {
        document.querySelector('.user-dropdown')?.remove();
        this.showNotification('Profile page coming soon!', 'info');
    }

    viewSettings() {
        document.querySelector('.user-dropdown')?.remove();
        this.showNotification('Settings page coming soon!', 'info');
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        const styles = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border: 1px solid #e2e8f0;
                border-left: 4px solid #6366f1;
                border-radius: 8px;
                padding: 16px 20px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: center;
                gap: 12px;
                max-width: 400px;
                z-index: 3000;
                animation: slideInRight 0.3s ease;
            }
            .notification-success { border-left-color: #10b981; }
            .notification-info { border-left-color: #3b82f6; }
            .notification i { color: #6366f1; }
            .notification-success i { color: #10b981; }
            .notification-info i { color: #3b82f6; }
            .notification-close {
                background: none;
                border: none;
                cursor: pointer;
                color: #a0aec0;
                font-size: 14px;
                padding: 4px;
            }
            .notification-close:hover { color: #4a5568; }
            @keyframes slideInRight {
                from { transform: translateX(400px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;

        if (!document.getElementById('notification-styles')) {
            const styleSheet = document.createElement('style');
            styleSheet.id = 'notification-styles';
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideInRight 0.3s ease reverse';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }
}

// Initialize dashboard when page loads
const dashboard = new Dashboard();