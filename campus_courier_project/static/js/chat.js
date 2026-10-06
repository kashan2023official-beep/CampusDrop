function chatPanel(orderId) {
  return {
    open: false,
    connected: false,
    messages: [],
    draft: '',
    ws: null,
    reconnectTimer: null,
    currentUserId: window.CURRENT_USER_ID || 0,

    openChat() {
      this.open = true;
      this.$nextTick(() => {
        this.scrollBottom();
        if (window.lucide) window.lucide.createIcons();
      });
      if (!this.ws) {
        this.loadHistory().then(() => this.connect());
      }
    },

    closeChat() {
      this.open = false;
    },

    async loadHistory() {
      try {
        const r = await fetch(`/api/order/${orderId}/messages/`, {
          credentials: 'same-origin',
        });
        if (!r.ok) return;
        const data = await r.json();
        if (data.messages) this.messages = data.messages;
      } catch (_) {}
    },

    connect() {
      const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
      const url = `${proto}://${window.location.host}/ws/order/${orderId}/chat/`;
      try {
        this.ws = new WebSocket(url);
      } catch (_) { return; }

      this.ws.onopen = () => { this.connected = true; };
      this.ws.onclose = () => {
        this.connected = false;
        this.scheduleReconnect();
      };
      this.ws.onerror = () => { try { this.ws.close(); } catch (_) {} };
      this.ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data);
          if (msg.type === 'message') this.receiveMessage(msg.data);
        } catch (_) {}
      };
    },

    scheduleReconnect() {
      if (this.reconnectTimer) return;
      this.reconnectTimer = setTimeout(() => {
        this.reconnectTimer = null;
        if (this.open) this.connect();
      }, 5000);
    },

    receiveMessage(m) {
      if (this.messages.some(x => x.id === m.id)) return;
      this.messages.push(m);
      this.$nextTick(() => {
        this.scrollBottom();
        if (window.lucide) window.lucide.createIcons();
      });
    },

    async send() {
      const body = this.draft.trim();
      if (!body) return;
      this.draft = '';

      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'message', body }));
        return;
      }

      // REST fallback when WS not available
      try {
        const token = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || '';
        const r = await fetch(`/api/order/${orderId}/messages/create/`, {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token,
          },
          body: JSON.stringify({ body }),
        });
        if (r.ok) {
          const data = await r.json();
          if (data.message) this.receiveMessage(data.message);
        }
      } catch (_) {}
    },

    scrollBottom() {
      const el = this.$refs.messages;
      if (el) el.scrollTop = el.scrollHeight;
    },

    formatTime(iso) {
      const d = new Date(iso);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
  };
}
