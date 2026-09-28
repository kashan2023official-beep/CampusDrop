function getBadgeClass(status) {
  switch (status) {
    case 'PENDING':
      return 'bg-amber-100 text-amber-800';
    case 'ACCEPTED':
      return 'bg-blue-100 text-blue-800';
    case 'PICKED_UP':
      return 'bg-indigo-100 text-indigo-800';
    case 'DELIVERED':
      return 'bg-emerald-100 text-emerald-800';
    case 'CANCELLED':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
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
        <div class="p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700 font-medium">
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

    if (step1) step1.className = `w-8 h-8 rounded-full flex items-center justify-center ${currentIdx >= 0 ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-600'}`;
    if (line1) line1.className = `flex-1 h-1 mx-2 ${currentIdx >= 1 ? 'bg-indigo-600' : 'bg-gray-200'}`;
    if (step2) step2.className = `w-8 h-8 rounded-full flex items-center justify-center ${currentIdx >= 1 ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-600'}`;
    if (line2) line2.className = `flex-1 h-1 mx-2 ${currentIdx >= 2 ? 'bg-indigo-600' : 'bg-gray-200'}`;
    if (step3) step3.className = `w-8 h-8 rounded-full flex items-center justify-center ${currentIdx >= 2 ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-600'}`;
    if (line3) line3.className = `flex-1 h-1 mx-2 ${currentIdx >= 3 ? 'bg-indigo-600' : 'bg-gray-200'}`;
    if (step4) step4.className = `w-8 h-8 rounded-full flex items-center justify-center ${currentIdx >= 3 ? 'bg-emerald-600 text-white' : 'bg-gray-200 text-gray-600'}`;
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
