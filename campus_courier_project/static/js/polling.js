function pollEvery(url, ms, onData) {
  let active = true;
  let timerId = null;

  async function execute() {
    if (!active) return;
    try {
      const response = await fetch(url, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Accept': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        if (active && typeof onData === 'function') {
          onData(data);
        }
      } else {
        console.warn(`Polling returned status ${response.status} for ${url}`);
      }
    } catch (err) {
      console.warn(`Polling error for ${url}:`, err);
    } finally {
      if (active) {
        timerId = setTimeout(execute, ms);
      }
    }
  }

  timerId = setTimeout(execute, ms);

  return function stop() {
    active = false;
    if (timerId) {
      clearTimeout(timerId);
    }
  };
}

if (typeof window !== 'undefined') {
  window.pollEvery = pollEvery;
}
