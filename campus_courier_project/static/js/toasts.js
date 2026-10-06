// static/js/toasts.js
document.addEventListener('DOMContentLoaded', () => {
  const scriptEl = document.getElementById('django-messages');
  const toastHost = document.getElementById('toast-host');
  if (!scriptEl || !toastHost) return;

  let messages = [];
  try {
    messages = JSON.parse(scriptEl.textContent);
  } catch (err) {
    console.error('Failed to parse django-messages JSON:', err);
    return;
  }

  if (!Array.isArray(messages) || messages.length === 0) return;

  function getToastConfig(tags) {
    const t = (tags || '').toLowerCase();
    if (t.includes('error')) {
      return {
        icon: 'alert-circle',
        iconBg: 'bg-brand-red/10',
        iconColor: 'text-brand-redDarkText',
      };
    }
    if (t.includes('warning')) {
      return {
        icon: 'alert-triangle',
        iconBg: 'bg-brand-yellow/20',
        iconColor: 'text-brand-yellowDark',
      };
    }
    if (t.includes('info') || t.includes('debug')) {
      return {
        icon: 'info',
        iconBg: 'bg-brand-blue/15',
        iconColor: 'text-brand-blueDarkText',
      };
    }
    // Default to success
    return {
      icon: 'check-circle-2',
      iconBg: 'bg-brand-greenTint',
      iconColor: 'text-brand-greenDarkText',
    };
  }

  function dismissToast(card, timerId) {
    if (timerId) clearTimeout(timerId);
    if (card.dataset.dismissing === 'true') return;
    card.dataset.dismissing = 'true';
    card.style.animation = 'slideOut 0.3s ease-out forwards';
    setTimeout(() => {
      card.remove();
    }, 300);
  }

  messages.forEach((msg) => {
    const config = getToastConfig(msg.tags);
    const card = document.createElement('div');
    card.className =
      'toast pointer-events-auto bg-white rounded-2xl shadow-lg p-4 flex items-start gap-3 animate-[slideIn_0.3s_ease-out]';

    // Build icon container
    const iconDiv = document.createElement('div');
    iconDiv.className = `w-9 h-9 rounded-full flex items-center justify-center shrink-0 ${config.iconBg}`;
    const iconEl = document.createElement('i');
    iconEl.setAttribute('data-lucide', config.icon);
    iconEl.className = `w-5 h-5 ${config.iconColor}`;
    iconDiv.appendChild(iconEl);

    // Build message container
    const textDiv = document.createElement('div');
    textDiv.className = 'flex-1 min-w-0';
    const textP = document.createElement('p');
    textP.className = 'text-sm font-medium text-brand-navy';
    textP.textContent = msg.message;
    textDiv.appendChild(textP);

    // Build close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'text-brand-navySubtext hover:text-brand-navy p-1';
    closeBtn.setAttribute('aria-label', 'Dismiss');
    const closeIcon = document.createElement('i');
    closeIcon.setAttribute('data-lucide', 'x');
    closeIcon.className = 'w-4 h-4';
    closeBtn.appendChild(closeIcon);

    card.appendChild(iconDiv);
    card.appendChild(textDiv);
    card.appendChild(closeBtn);

    toastHost.appendChild(card);

    const timerId = setTimeout(() => {
      dismissToast(card, timerId);
    }, 4000);

    closeBtn.addEventListener('click', () => {
      dismissToast(card, timerId);
    });
  });

  if (window.lucide) {
    window.lucide.createIcons();
  }
});
