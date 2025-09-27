// Modern JavaScript for GIFverse

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Focus on URL input by default
    const urlInput = document.getElementById('url');
    if (urlInput) {
        urlInput.focus();
    }

    // Form handling
    const form = document.getElementById('gifForm');
    const submitBtn = document.getElementById('submitBtn');
    const fileInput = document.getElementById('gif');
    const urlInputField = document.getElementById('url');

    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                // Clear URL input when file is selected
                if (urlInputField) {
                    urlInputField.value = '';
                }

                // Validate file type
                if (!file.type.startsWith('image/gif')) {
                    showAlert('Please select a valid GIF file.', 'danger');
                    e.target.value = '';
                    return;
                }

                // Validate file size (15MB limit)
                const maxSize = 15 * 1024 * 1024; // 15MB
                if (file.size > maxSize) {
                    showAlert('File size must be less than 15MB.', 'danger');
                    e.target.value = '';
                    return;
                }

                showAlert('File selected successfully!', 'success');
            }
        });
    }

    // URL input change handler
    if (urlInputField) {
        urlInputField.addEventListener('input', (e) => {
            const url = e.target.value.trim();
            if (url) {
                // Clear file input when URL is entered
                if (fileInput) {
                    fileInput.value = '';
                }

                // Basic URL validation
                if (isValidUrl(url)) {
                    showAlert('URL looks good!', 'success');
                } else if (url.length > 5) {
                    showAlert('Please enter a valid URL.', 'warning');
                }
            }
        });
    }

    // Form submission handler
    if (form) {
        form.addEventListener('submit', (e) => {
            const file = fileInput ? fileInput.files[0] : null;
            const url = urlInputField ? urlInputField.value.trim() : '';

            // Validate that either file or URL is provided
            if (!file && !url) {
                e.preventDefault();
                showAlert('Please provide either a GIF file or a URL.', 'danger');
                return;
            }

            // Show loading state
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
            }
        });
    }

    // Download functionality for main page
    window.downloadGifMain = function() {
        const gifImg = document.querySelector('#gifversed img');
        if (gifImg) {
            const link = document.createElement('a');
            link.href = gifImg.src;
            link.download = 'seamless-gif.gif';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
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

    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
                entry.target.style.opacity = '1';
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        observer.observe(card);
    });

    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'translateY(-2px)';
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translateY(0)';
        });
    });

    // Add click animation to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.style.transform = 'translateY(0) scale(0.98)';
            setTimeout(() => {
                btn.style.transform = 'translateY(-2px) scale(1)';
            }, 150);
        });
    });
});

// Utility functions
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        // Check if it's a URL without protocol
        const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
        return urlPattern.test(string);
    }
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');

    const icon = getAlertIcon(type);
    alertDiv.innerHTML = `
        ${icon} ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert alert at the top of the form
    const form = document.getElementById('gifForm');
    if (form) {
        form.insertBefore(alertDiv, form.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function getAlertIcon(type) {
    const icons = {
        'success': '<i class="fas fa-check-circle me-2"></i>',
        'danger': '<i class="fas fa-exclamation-triangle me-2"></i>',
        'warning': '<i class="fas fa-exclamation-circle me-2"></i>',
        'info': '<i class="fas fa-info-circle me-2"></i>'
    };
    return icons[type] || icons['info'];
}

// Add some fun animations
function addPulseAnimation(element) {
    element.style.animation = 'pulse 2s infinite';
}

function removePulseAnimation(element) {
    element.style.animation = '';
}

// Add loading state to form
function setFormLoading(loading) {
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        if (loading) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitBtn.disabled = true;
            addPulseAnimation(submitBtn);
        } else {
            submitBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Create Seamless GIF';
            submitBtn.disabled = false;
            removePulseAnimation(submitBtn);
        }
    }
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('gifForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }

    // Escape to clear form
    if (e.key === 'Escape') {
        const fileInput = document.getElementById('gif');
        const urlInput = document.getElementById('url');

        if (fileInput) fileInput.value = '';
        if (urlInput) urlInput.value = '';

        // Remove any alerts
        document.querySelectorAll('.alert').forEach(alert => alert.remove());
    }
});

// Add drag and drop functionality for file input
const fileInput = document.getElementById('gif');
if (fileInput) {
    const dropZone = fileInput.closest('.col-md-6');

    if (dropZone) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    }
}

// Add CSS for drag and drop
const style = document.createElement('style');
style.textContent = `
    .drag-over {
        background-color: rgba(13, 110, 253, 0.1) !important;
        border: 2px dashed #0d6efd !important;
        border-radius: 0.5rem !important;
    }
`;
document.head.appendChild(style);
