// Dashboard JavaScript Functions

// Toggle Sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    
    if (!sidebar) {
        console.warn('Sidebar element not found. Looking for element with id="sidebar"');
        return;
    }
    
    // Toggle the collapsed class
    const isCollapsed = sidebar.classList.toggle('collapsed');
    
    // Save state to localStorage
    localStorage.setItem('sidebarCollapsed', isCollapsed.toString());
    
    // Debug info
    console.log('Sidebar toggled. Collapsed:', isCollapsed);
    console.log('Sidebar classes:', sidebar.className);
}

// Load sidebar collapsed state
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) {
        console.warn('Sidebar element not found during DOMContentLoaded');
        return;
    }
    
    const savedState = localStorage.getItem('sidebarCollapsed');
    const isCollapsed = savedState === 'true';
    
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
        console.log('Sidebar restored from localStorage as collapsed');
    } else {
        sidebar.classList.remove('collapsed');
        console.log('Sidebar restored from localStorage as expanded');
    }

    // Set active nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });
});

// Show custom notification (for AJAX responses)
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `dashboard-message`;
    notification.innerHTML = `
        <div class="message-alert ${type}">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.insertBefore(notification, document.body.firstChild);
}

// AJAX function to load content
function loadContent(url, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '<div class="loading">Loading...</div>';

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.text();
        })
        .then(data => {
            container.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML = '<div class="error">Error loading content. Please refresh the page.</div>';
        });
}

// Logout confirmation
function confirmLogout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/accounts/logout/';
    }
}

// Update complaint status via AJAX (no page reload)
function updateComplaintStatus(complaintId) {
    const statusSelect = document.getElementById('status-' + complaintId);
    const tableRow = document.getElementById('complaint-row-' + complaintId);
    
    if (!statusSelect) return;

    const newStatus = statusSelect.value;
    
    fetch(`/complaint-update/${complaintId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
        },
        body: `status=${newStatus}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Status updated successfully!', 'success');
            
            // Update only the specific row if it exists
            if (tableRow) {
                const badgeCell = tableRow.querySelector('td:nth-child(3)');
                if (badgeCell) {
                    const statusClass = newStatus === 'resolved' ? 'badge-success' : 
                                      newStatus === 'in_progress' ? 'badge-progress' : 'badge-pending';
                    const statusText = newStatus === 'resolved' ? 'Resolved' : 
                                     newStatus === 'in_progress' ? 'In Progress' : 'Pending';
                    badgeCell.innerHTML = `<span class="badge ${statusClass}">${statusText}</span>`;
                }
            }
        } else {
            showNotification('Error updating status', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    });
}
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 90px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideInRight 0.3s ease;
        }
        .notification-success {
            background: #10b981;
        }
        .notification-error {
            background: #ef4444;
        }
        .notification-info {
            background: #3b82f6;
        }
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Filter table rows
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    const filter = input.value.toUpperCase();
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const text = rows[i].textContent.toUpperCase();
        rows[i].style.display = text.includes(filter) ? '' : 'none';
    }
}
