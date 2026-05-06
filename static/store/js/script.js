function addToCart(productId) {
    fetch(`/add_to_cart/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCount(data.cart_count);
            showNotification('✅ ' + data.message, 'success');
        } else {
            showNotification('❌ ' + data.message, 'error');
        }
    })
    .catch(error => {
        showNotification('❌ Error adding to cart', 'error');
    });
}

function buyNow(productId) {
    window.location.href = `/buy_now/${productId}/`;
}

function updateCartCount(count) {
    const badge = document.getElementById('cart-count');
    if (badge) {
        badge.textContent = count;
        badge.setAttribute('aria-label', `${count} items in cart`);
        badge.classList.add('pulse');
        window.setTimeout(() => badge.classList.remove('pulse'), 250);
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.setAttribute('role', 'status');
    notification.setAttribute('aria-live', 'polite');
    notification.setAttribute('aria-atomic', 'true');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        ${type === 'success' ? 'background: #dcfce7; color: #065f46;' : 'background: #fee2e2; color: #991b1b;'}
        box-shadow: 0 16px 48px rgba(15, 23, 42, 0.18);
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2600);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(30px); opacity: 0; }
    }
`;
document.head.appendChild(style);