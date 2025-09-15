document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navButtons = document.querySelector('.nav-buttons');

    hamburger?.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        navButtons.classList.toggle('active');
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .pricing-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    const pricingCards = document.querySelectorAll('.pricing-card:not(.featured)');
    pricingCards.forEach(card => {
        const button = card.querySelector('.btn');
        button?.addEventListener('click', function() {
            showNotification('Feature coming soon! Stay tuned for updates.', 'info');
        });
    });

    document.querySelector('.pricing-card.featured .btn')?.addEventListener('click', function() {
        openModal('signupModal');
    });

    const loginForm = document.querySelector('#loginModal .auth-form');
    const signupForm = document.querySelector('#signupModal .auth-form');

    loginForm?.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (email && password) {
            showNotification('Login functionality will be connected to backend!', 'success');
            setTimeout(() => {
                closeModal('loginModal');
            }, 1500);
        }
    });

    signupForm?.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;

        if (name && email && password) {
            showNotification('Account creation will be connected to backend!', 'success');
            setTimeout(() => {
                closeModal('signupModal');
            }, 1500);
        }
    });
});

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';

        setTimeout(() => {
            modal.querySelector('.modal-content').style.transform = 'translateY(0)';
            modal.querySelector('.modal-content').style.opacity = '1';
        }, 10);
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.querySelector('.modal-content').style.transform = 'translateY(-50px)';
        modal.querySelector('.modal-content').style.opacity = '0';

        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }, 300);
    }
}

function switchModal(currentModalId, targetModalId) {
    closeModal(currentModalId);
    setTimeout(() => {
        openModal(targetModalId);
    }, 300);
}

function playDemo() {
    showNotification('Demo video coming soon! Contact us for a live demo.', 'info');
}

function showNotification(message, type = 'info') {
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

        .notification-success {
            border-left-color: #10b981;
        }

        .notification-info {
            border-left-color: #3b82f6;
        }

        .notification i {
            color: #6366f1;
        }

        .notification-success i {
            color: #10b981;
        }

        .notification-info i {
            color: #3b82f6;
        }

        .notification-close {
            background: none;
            border: none;
            cursor: pointer;
            color: #a0aec0;
            font-size: 14px;
            padding: 4px;
        }

        .notification-close:hover {
            color: #4a5568;
        }

        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
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

window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            closeModal(modal.id);
        }
    });
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const openModal = document.querySelector('.modal[style*="block"]');
        if (openModal) {
            closeModal(openModal.id);
        }
    }
});

const typeWriter = {
    text: '',
    speed: 100,
    element: null,

    init(element, text, speed = 100) {
        this.element = element;
        this.text = text;
        this.speed = speed;
        this.element.textContent = '';
        this.type();
    },

    type() {
        let i = 0;
        const timer = setInterval(() => {
            this.element.textContent += this.text.charAt(i);
            i++;
            if (i >= this.text.length) {
                clearInterval(timer);
            }
        }, this.speed);
    }
};

document.querySelectorAll('.chart-bar').forEach((bar, index) => {
    bar.style.animationDelay = `${index * 0.2}s`;
});

let ticking = false;
function updateScrollProgress() {
    if (!ticking) {
        requestAnimationFrame(() => {
            const scrolled = window.pageYOffset;
            const rate = scrolled / (document.body.scrollHeight - window.innerHeight);
            const progressBar = document.querySelector('.scroll-progress');
            if (progressBar) {
                progressBar.style.transform = `scaleX(${rate})`;
            }
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener('scroll', updateScrollProgress);

const createScrollProgress = () => {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 70px;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        transform-origin: 0;
        transform: scaleX(0);
        z-index: 999;
        transition: transform 0.1s ease;
    `;
    document.body.appendChild(progressBar);
};

if (window.innerWidth > 768) {
    createScrollProgress();
}