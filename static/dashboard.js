// ============================================
// SIDEBAR TOGGLE - BULLETPROOF VERSION
// ============================================

let sidebarState = null; // null = not initialized

function initializeSidebarState() {
    // Get saved state from localStorage
    const saved = localStorage.getItem('sidebarCollapsed');
    sidebarState = saved === 'true' ? true : false;
    console.log('[INIT] Sidebar state initialized:', sidebarState);
    applySidebarState();
}

function applySidebarState() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (!sidebar || !mainContent) {
        console.error('[APPLY] ERROR: Elements missing');
        return;
    }
    
    if (sidebarState === true) {
        // COLLAPSED STATE - NO GAP ON RIGHT
        sidebar.classList.add('collapsed');
        mainContent.style.setProperty('margin-left', '70px', 'important');
        mainContent.style.setProperty('width', 'calc(100% - 70px)', 'important');
        console.log('[APPLY] Applied COLLAPSED state');
    } else {
        // EXPANDED STATE
        sidebar.classList.remove('collapsed');
        mainContent.style.setProperty('margin-left', '280px', 'important');
        mainContent.style.setProperty('width', 'calc(100% - 280px)', 'important');
        console.log('[APPLY] Applied EXPANDED state');
    }
}

function toggleSidebar() {
    console.log('=== TOGGLE CALLED ===');
    console.log('Current state:', sidebarState);
    
    // Flip the state
    sidebarState = !sidebarState;
    console.log('New state:', sidebarState);
    
    // Save to localStorage
    localStorage.setItem('sidebarCollapsed', sidebarState.toString());
    console.log('Saved to localStorage');
    
    // Apply the new state
    applySidebarState();
    
    console.log('=== TOGGLE COMPLETE ===');
}

// Early initialization - as soon as script loads
console.log('[EARLY-INIT] Script loaded');
if (document.readyState === 'loading') {
    // DOM is still loading
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[DOMContentLoaded] Initializing sidebar');
        initializeSidebarState();
        setActiveNavItem();
    });
} else {
    // DOM is already loaded
    console.log('[READY] DOM already loaded, initializing now');
    initializeSidebarState();
    setActiveNavItem();
}

function setActiveNavItem() {
    const currentPath = window.location.pathname;
    console.log('[NAV] Current path:', currentPath);
    
    document.querySelectorAll('.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href === currentPath) {
            item.classList.add('active');
            console.log('[NAV] Set active:', href);
        }
    });
}

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
