// static/js/available.js
let firstLoad = true;

function getCsrfToken() {
  const input = document.querySelector('[name=csrfmiddlewaretoken]');
  if (input) return input.value;
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

function renderAvailableOrders(orders) {
  const container = document.getElementById('available-list');
  const skeleton = document.getElementById('available-skeleton');

  if (firstLoad) {
    firstLoad = false;
    if (skeleton) skeleton.classList.add('hidden');
    if (container) container.classList.remove('hidden');
  }

  if (!container) return;

  if (!orders || orders.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center bg-white rounded-2xl shadow-sm text-brand-navySubtext space-y-2">
        <div class="w-12 h-12 rounded-full bg-brand-greenTint flex items-center justify-center mx-auto text-brand-greenDarkText mb-2">
          <i data-lucide="truck" class="w-6 h-6"></i>
        </div>
        <p class="text-sm font-medium text-brand-navy">No pending orders right now.</p>
        <p class="text-xs text-brand-navySubtext">Check again soon. This page refreshes every 5 seconds.</p>
      </div>
    `;
    if (window.lucide) {
      window.lucide.createIcons();
    }
    return;
  }

  const csrfToken = getCsrfToken();

  container.innerHTML = orders
    .map(
      (order) => `
    <div class="bg-white rounded-2xl shadow-sm p-5 space-y-4">
      <div class="flex items-start gap-3">
        <div class="w-12 h-12 rounded-full bg-brand-yellow/20 flex items-center justify-center shrink-0">
          <i data-lucide="package" class="w-6 h-6 text-brand-yellowDark"></i>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-[10px] uppercase tracking-wide text-brand-navySubtext flex items-center gap-2">
            Pickup
            <span class="inline-flex items-center gap-0.5 text-xs text-brand-navySubtext normal-case tracking-normal">
              <i data-lucide="star" class="w-3 h-3 text-brand-yellow fill-brand-yellow"></i>
              ${order.sender_rating ? order.sender_rating.toFixed(1) : '5.0'}
            </span>
          </p>
          <p class="text-sm font-semibold text-brand-navy truncate">${order.pickup_label || 'Campus Pickup'}</p>
          <p class="text-[10px] uppercase tracking-wide text-brand-navySubtext mt-2">Dropoff</p>
          <p class="text-sm font-semibold text-brand-navy truncate">${order.dropoff_label || 'Campus Dropoff'}</p>
        </div>
      </div>
      <div class="grid grid-cols-3 gap-3 pt-3 border-t border-brand-grey text-xs">
        <div>
          <p class="text-[10px] uppercase text-brand-navySubtext">Fare</p>
          <p class="font-semibold text-brand-navy">Rs ${order.predicted_fare ? order.predicted_fare.toFixed(0) : '0'}</p>
        </div>
        <div>
          <p class="text-[10px] uppercase text-brand-navySubtext">Distance</p>
          <p class="font-semibold text-brand-navy">${order.distance_km ? order.distance_km.toFixed(1) : '0.0'} km</p>
        </div>
        <div>
          <p class="text-[10px] uppercase text-brand-navySubtext">Weight</p>
          <p class="font-semibold text-brand-navy">${order.weight_kg} kg</p>
        </div>
      </div>
      <form method="post" action="/courier/accept/${order.id}/">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <button type="submit"
                class="js-loading-btn w-full py-3 rounded-full bg-brand-green text-white text-sm font-medium
                       active:scale-[0.98] transition-transform hover:bg-brand-greenDark focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-greenDark focus-visible:ring-offset-2">
          Accept Order
        </button>
      </form>
    </div>
  `
    )
    .join('');

  if (window.lucide) {
    window.lucide.createIcons();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('available-list');
  const skeleton = document.getElementById('available-skeleton');

  if (container && skeleton) {
    skeleton.classList.remove('hidden');
    container.classList.add('hidden');
  }

  // Fetch immediately on initial load
  fetch('/courier/available/json/', {
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'Accept': 'application/json',
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((data) => renderAvailableOrders(data))
    .catch((err) => {
      console.warn('Initial orders fetch failed:', err);
      if (firstLoad) {
        firstLoad = false;
        if (skeleton) skeleton.classList.add('hidden');
        if (container) container.classList.remove('hidden');
      }
    });

  if (container && typeof pollEvery === 'function') {
    pollEvery('/courier/available/json/', 5000, renderAvailableOrders);
  }
});
