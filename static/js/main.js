// ============================================
// WASTE MANAGEMENT SYSTEM - Enhanced JavaScript
// Professional UI/UX Interactions
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initializeTooltips();
    initializePopovers();
    initializeNavbar();
    initializeAnimations();
    initializeFormValidation();
    autoHideAlerts();

    console.log('✅ Waste Management System loaded successfully');
});

// ============================================
// BOOTSTRAP COMPONENTS INITIALIZATION
// ============================================

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            animation: true,
            delay: { show: 300, hide: 100 }
        });
    });
}

function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'hover focus',
            animation: true
        });
    });
}

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================

function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ============================================
// PAGE ANIMATIONS
// ============================================

function initializeAnimations() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main') || document.querySelector('.container');
    if (mainContent) {
        mainContent.classList.add('animate-fade-in');
    }

    // Animate cards with stagger effect
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('card-animate');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Animate stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.classList.add('animate-fade-in-up');
        card.style.animationDelay = `${index * 0.15}s`;
    });

    // Add hover lift effect to interactive elements
    const liftElements = document.querySelectorAll('.card, .btn');
    liftElements.forEach(el => {
        el.classList.add('hover-lift');
    });
}

// ============================================
// FORM VALIDATION & ENHANCEMENT
// ============================================

function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation, form');

    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                // Show error toast
                showToast('Please fill in all required fields', 'error');
            }
            form.classList.add('was-validated');
        }, false);

        // Add animation to form controls
        const formControls = form.querySelectorAll('.form-control, .form-select');
        formControls.forEach(control => {
            control.classList.add('form-control-animated');
        });
    });
}

// ============================================
// IMAGE PREVIEW
// ============================================

function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const preview = document.getElementById(previewId);

        reader.onload = function (e) {
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                preview.classList.add('animate-scale-in');
            }
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// ============================================
// TOAST NOTIFICATIONS
// ============================================

function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();

    const toastId = 'toast-' + Date.now();
    const iconMap = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        warning: 'bi-exclamation-triangle-fill',
        info: 'bi-info-circle-fill'
    };

    const colorMap = {
        success: 'success',
        error: 'danger',
        warning: 'warning',
        info: 'info'
    };

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${colorMap[type]} border-0 toast-enter" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconMap[type]} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });

    toast.show();

    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });
}

function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    return container;
}

// ============================================
// AUTO-HIDE ALERTS
// ============================================

function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');

    alerts.forEach(alert => {
        // Add entrance animation
        alert.classList.add('animate-fade-in-right');

        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            alert.classList.add('animate-fade-out');
            setTimeout(() => {
                bsAlert.close();
            }, 300);
        }, 5000);
    });
}

// ============================================
// LOADING SPINNER
// ============================================

function showLoading(buttonId) {
    const btn = document.getElementById(buttonId);
    if (btn) {
        btn.disabled = true;
        const originalText = btn.innerHTML;
        btn.setAttribute('data-original-text', originalText);
        btn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Loading...
        `;
    }
}

function hideLoading(buttonId) {
    const btn = document.getElementById(buttonId);
    if (btn) {
        btn.disabled = false;
        const originalText = btn.getAttribute('data-original-text');
        if (originalText) {
            btn.innerHTML = originalText;
        }
    }
}

// ============================================
// CONFIRM DIALOGS
// ============================================

function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item? This action cannot be undone.');
}

function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

// ============================================
// TABLE SEARCH/FILTER
// ============================================

function filterTable(searchInputId, tableId) {
    const input = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);

    if (!input || !table) return;

    const filter = input.value.toUpperCase();
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const txtValue = cell.textContent || cell.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }

        rows[i].style.display = found ? '' : 'none';
    }
}

// ============================================
// SMOOTH SCROLL
// ============================================

function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ============================================
// COPY TO CLIPBOARD
// ============================================

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy', 'error');
    });
}

// ============================================
// NUMBER COUNTER ANIMATION
// ============================================

function animateCounter(elementId, target, duration = 2000) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// ============================================
// RIPPLE EFFECT
// ============================================

function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');

    const ripple = button.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }

    button.appendChild(circle);
}

// Add ripple effect to all buttons
document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
});

// ============================================
// INTERSECTION OBSERVER - Lazy Animations
// ============================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with lazy-animate class
document.addEventListener('DOMContentLoaded', function () {
    const lazyElements = document.querySelectorAll('.lazy-animate');
    lazyElements.forEach(el => observer.observe(el));
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// ============================================
// EXPORT FUNCTIONS
// ============================================

window.WasteManagement = {
    showToast,
    showLoading,
    hideLoading,
    confirmDelete,
    confirmAction,
    filterTable,
    smoothScrollTo,
    copyToClipboard,
    animateCounter,
    previewImage,
    formatNumber,
    debounce
};
