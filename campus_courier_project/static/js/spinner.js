// static/js/spinner.js
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('submit', (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    // Check if the form has a button with .js-loading-btn OR form itself has .js-loading-btn
    let btn = form.querySelector('button.js-loading-btn, input[type="submit"].js-loading-btn');
    if (!btn && form.classList.contains('js-loading-btn')) {
      btn = form.querySelector('button[type="submit"], input[type="submit"]') || form.querySelector('button');
    }

    if (btn && !btn.dataset.loadingApplied) {
      btn.dataset.loadingApplied = 'true';

      const spinnerSvg = `
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 inline-block align-text-bottom" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      `;

      btn.innerHTML = `${spinnerSvg}<span>Please wait...</span>`;
      btn.classList.add('opacity-75', 'cursor-not-allowed');

      // Disable briefly after form submission initiates to ensure browser dispatches POST
      setTimeout(() => {
        btn.disabled = true;
      }, 10);
    }
  });
});
