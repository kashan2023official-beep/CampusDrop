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
      <div class="p-8 text-center bg-white rounded-lg border border-gray-200 text-gray-500 shadow-sm">
        <p class="text-base font-medium">No pending orders right now. This page refreshes every 5 seconds.</p>
      </div>
    `;
    return;
  }

  const csrfToken = getCsrfToken();

  container.innerHTML = orders
    .map(
      (order) => `
    <div class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="space-y-1">
        <div class="flex items-center space-x-2">
          <span class="font-bold text-gray-900 text-base">#${order.id}</span>
          <span class="text-xs px-2 py-0.5 rounded-full font-semibold bg-amber-100 text-amber-800">Pending</span>
          <span class="text-xs text-gray-400">&bull; ${order.item_type}</span>
        </div>
        <div class="text-sm text-gray-700">
          <span class="font-medium text-gray-900">Pickup:</span> ${order.pickup_label || 'Campus Pickup'} &rarr;
          <span class="font-medium text-gray-900">Dropoff:</span> ${order.dropoff_label || 'Campus Dropoff'}
        </div>
        <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-gray-500 pt-1">
          <span><strong>Weight:</strong> ${order.weight_kg} kg</span>
          <span><strong>Distance:</strong> ${order.distance_km} km</span>
          <span><strong>Fare:</strong> PKR ${order.predicted_fare ? order.predicted_fare.toFixed(0) : 'TBD'}</span>
        </div>
      </div>
      <div>
        <form method="post" action="/courier/accept/${order.id}/" class="inline">
          <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
          <button type="submit" class="js-loading-btn w-full md:w-auto px-5 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md shadow-sm hover:bg-indigo-700 transition">
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
