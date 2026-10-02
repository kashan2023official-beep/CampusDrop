function getCsrfToken() {
  const input = document.querySelector('[name=csrfmiddlewaretoken]');
  if (input) return input.value;
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

function renderAvailableOrders(orders) {
  const container = document.getElementById('available-list');
  if (!container) return;

  if (!orders || orders.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center bg-white rounded-lg border border-brand-grey text-brand-navySubtext shadow-sm">
        <p class="text-base font-medium">No pending orders right now. This page refreshes every 5 seconds.</p>
      </div>
    `;
    return;
  }

  const csrfToken = getCsrfToken();

  container.innerHTML = orders
    .map(
      (order) => `
    <div class="bg-white p-5 rounded-lg border border-brand-grey shadow-sm flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="space-y-1">
        <div class="flex items-center space-x-2">
          <span class="font-bold text-brand-navy text-base">#${order.id}</span>
          <span class="text-xs px-2 py-0.5 rounded-full font-semibold bg-brand-yellow/20 text-brand-yellowDark">Pending</span>
          <span class="text-xs text-brand-greyDark">&bull; ${order.item_type}</span>
        </div>
        <div class="text-sm text-brand-navySubtext">
          <span class="font-medium text-brand-navy">Pickup:</span> ${order.pickup_label || 'Campus Pickup'} &rarr;
          <span class="font-medium text-brand-navy">Dropoff:</span> ${order.dropoff_label || 'Campus Dropoff'}
        </div>
        <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-brand-navySubtext pt-1">
          <span><strong>Weight:</strong> ${order.weight_kg} kg</span>
          <span><strong>Distance:</strong> ${order.distance_km} km</span>
          <span><strong>Fare:</strong> PKR ${order.predicted_fare ? order.predicted_fare.toFixed(0) : 'TBD'}</span>
        </div>
      </div>
      <div>
        <form method="post" action="/courier/accept/${order.id}/" class="inline">
          <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
          <button type="submit" class="js-loading-btn w-full md:w-auto min-h-touch px-5 py-2 text-sm font-semibold text-brand-navy bg-brand-green rounded-md shadow-sm hover:bg-brand-greenDark transition inline-flex items-center justify-center">
            Accept Order
          </button>
        </form>
      </div>
    </div>
  `
    )
    .join('');
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('available-list');
  if (container && typeof pollEvery === 'function') {
    pollEvery('/courier/available/json/', 5000, renderAvailableOrders);
  }
});
