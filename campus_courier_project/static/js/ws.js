(function () {
  'use strict';

  function wsUrl(path) {
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
    return `${proto}://${window.location.host}${path}`;
  }

  function connect(url, options) {
    const onMessage = options && options.onMessage;
    const onOpen = options && options.onOpen;
    let ws = null;
    let stopped = false;
    let reconnectTimer = null;
    let pingTimer = null;

    function open() {
      try {
        ws = new WebSocket(url);
      } catch (e) {
        schedule();
        return;
      }

      ws.onopen = function () {
        pingTimer = setInterval(function () {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
          }
        }, 15000);
        if (onOpen) onOpen();
      };

      ws.onmessage = function (e) {
        try {
          const msg = JSON.parse(e.data);
          if (onMessage) onMessage(msg);
        } catch (_) { /* ignore malformed */ }
      };

      ws.onclose = function () {
        clearInterval(pingTimer);
        schedule();
      };

      ws.onerror = function () {
        try { ws.close(); } catch (_) {}
      };
    }

    function schedule() {
      if (stopped || reconnectTimer) return;
      reconnectTimer = setTimeout(function () {
        reconnectTimer = null;
        open();
      }, 5000);
    }

    open();

    return {
      close: function () {
        stopped = true;
        clearTimeout(reconnectTimer);
        clearInterval(pingTimer);
        try { if (ws) ws.close(); } catch (_) {}
      },
    };
  }

  window.CourierWS = {
    connectOrderStatus: function (orderId, onStatus) {
      return connect(wsUrl('/ws/order/' + orderId + '/'), {
        onMessage: function (m) {
          if (m.type === 'status') onStatus(m.data);
        },
      });
    },
    connectCourierFeed: function (onEvent) {
      return connect(wsUrl('/ws/courier/available/'), { onMessage: onEvent });
    },
  };
})();
