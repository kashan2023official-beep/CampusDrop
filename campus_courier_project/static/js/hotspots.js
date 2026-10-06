document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('available-map') || document.getElementById('map');
    if (!mapElement) return;

    fetch('/api/campus-bounds/')
        .then(res => res.json())
        .then(boundsData => {
            const map = L.map(mapElement).setView(boundsData.center, 15);
            L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                maxZoom: 19,
                attribution: '© Esri'
            }).addTo(map);

            L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
                maxZoom: 19,
            }).addTo(map);

            fetch('/api/hotspots/')
                .then(res => res.json())
                .then(data => {
                    if (!data.available || data.hotspots.length === 0) {
                        const overlay = document.createElement('div');
                        overlay.className = 'absolute inset-0 z-[400] flex items-center justify-center bg-white/50 backdrop-blur-sm rounded-2xl';
                        overlay.innerHTML = '<p class="text-sm font-medium text-brand-navySubtext bg-white px-4 py-2 rounded-full shadow-sm text-center">Not enough data yet — hotspots will appear after more deliveries.</p>';
                        mapElement.parentElement.classList.add('relative');
                        mapElement.parentElement.appendChild(overlay);
                        return;
                    }

                    data.hotspots.forEach(h => {
                        const circle = L.circle([h.centroid_lat, h.centroid_lon], {
                            radius: h.radius_km * 1000,
                            color: '#FF5400',
                            fillColor: '#FF931E',
                            fillOpacity: 0.25,
                            weight: 2
                        }).addTo(map);

                        const countText = h.count > 1 ? 'pickups' : 'pickup';
                        circle.bindTooltip(`${h.label} · ${h.count} ${countText}`);
                    });
                })
                .catch(err => console.error("Error fetching hotspots:", err));
        })
        .catch(err => console.error("Error fetching bounds:", err));
});
