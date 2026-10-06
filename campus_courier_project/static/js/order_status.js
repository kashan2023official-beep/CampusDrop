function getBadgeClass(status) {
  switch (status) {
    case 'PENDING':
      return 'bg-brand-yellow/20 text-brand-yellowDark';
    case 'ACCEPTED':
      return 'bg-brand-blue/20 text-brand-blueDarkText';
    case 'PICKED_UP':
      return 'bg-brand-purple/15 text-brand-purple';
    case 'DELIVERED':
      return 'bg-brand-green/20 text-brand-greenDarkText';
    case 'CANCELLED':
      return 'bg-brand-red/15 text-brand-redDarkText';
    default:
      return 'bg-brand-greyLight text-brand-navySubtext';
  }
}

function updateOrderStatus(data) {
  if (!data || !data.status) return;

  const badge = document.getElementById('status-badge');
  if (badge) {
    badge.textContent = data.status.replace('_', ' ');
    badge.className =
      'inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ' +
      getBadgeClass(data.status);
  }

  const timeline = document.getElementById('status-timeline');
  if (timeline) {
    if (data.status === 'CANCELLED') {
      timeline.innerHTML = `
        <div class="p-3 bg-brand-red/10 border border-brand-red/30 rounded-md text-sm text-brand-redDarkText font-medium">
          This order has been cancelled.
        </div>
      `;
      return;
    }

    const stepOrder = ['PENDING', 'ACCEPTED', 'PICKED_UP', 'DELIVERED'];
    const currentIdx = stepOrder.indexOf(data.status);

    const step1 = document.getElementById('timeline-step-1');
    const step2 = document.getElementById('timeline-step-2');
    const step3 = document.getElementById('timeline-step-3');
    const step4 = document.getElementById('timeline-step-4');

    const line1 = document.getElementById('timeline-line-1');
    const line2 = document.getElementById('timeline-line-2');
    const line3 = document.getElementById('timeline-line-3');

    if (step1) step1.className = `w-8 h-8 rounded-full flex items-center justify-center font-semibold text-xs ${currentIdx >= 0 ? 'bg-brand-green text-brand-navy' : 'bg-brand-grey text-brand-navySubtext'}`;
    if (line1) line1.className = `flex-1 h-1 mx-2 ${currentIdx >= 1 ? 'bg-brand-green' : 'bg-brand-grey'}`;
    if (step2) step2.className = `w-8 h-8 rounded-full flex items-center justify-center font-semibold text-xs ${currentIdx >= 1 ? 'bg-brand-green text-brand-navy' : 'bg-brand-grey text-brand-navySubtext'}`;
    if (line2) line2.className = `flex-1 h-1 mx-2 ${currentIdx >= 2 ? 'bg-brand-green' : 'bg-brand-grey'}`;
    if (step3) step3.className = `w-8 h-8 rounded-full flex items-center justify-center font-semibold text-xs ${currentIdx >= 2 ? 'bg-brand-green text-brand-navy' : 'bg-brand-grey text-brand-navySubtext'}`;
    if (line3) line3.className = `flex-1 h-1 mx-2 ${currentIdx >= 3 ? 'bg-brand-green' : 'bg-brand-grey'}`;
    if (step4) step4.className = `w-8 h-8 rounded-full flex items-center justify-center font-semibold text-xs ${currentIdx >= 3 ? 'bg-brand-green text-brand-navy' : 'bg-brand-grey text-brand-navySubtext'}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('order-status-root');
  if (root) {
    const orderId = root.getAttribute('data-order-id');
    if (orderId && typeof pollEvery === 'function') {
      pollEvery(`/api/order/${orderId}/status/`, 5000, updateOrderStatus);
    }
  }
});

// WebSocket upgrade — lowers latency when available
(function () {
  function initWS() {
    if (!window.CourierWS) return;
    const rootEl = document.getElementById('order-status-root');
    if (!rootEl) return;
    const orderId = rootEl.getAttribute('data-order-id');
    if (!orderId) return;
    try {
      window.CourierWS.connectOrderStatus(orderId, function (data) {
        if (data) updateOrderStatus(data);
      });
    } catch (_) {
      // Keep polling as fallback. Silently ignore.
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWS);
  } else {
    initWS();
  }
})();

