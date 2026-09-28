
export function initStaticMaps(selector) {
  const elements = document.querySelectorAll(selector);
  if (elements.length === 0) return;

  fetch('/api/campus-bounds/')
    .then(r => r.json())
    .then(data => {
      const bounds = data.bounds;

      elements.forEach(el => {
        const pickupStr = el.dataset.pickup;
        const dropoffStr = el.dataset.dropoff;

        if (!pickupStr || !dropoffStr) return;

        const pParts = pickupStr.split(',');
        const dParts = dropoffStr.split(',');
        
        const pickupLat = parseFloat(pParts[0]);
        const pickupLon = parseFloat(pParts[1]);
        const dropoffLat = parseFloat(dParts[0]);
        const dropoffLon = parseFloat(dParts[1]);

        // Setup Leaflet map for this element
        const map = L.map(el, {
          zoomControl: false,
          dragging: false,
          scrollWheelZoom: false,
          doubleClickZoom: false,
          boxZoom: false,
          touchZoom: false,
          keyboard: false,
          minZoom: 15,
          maxZoom: 19
        });

        const satelliteBase = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community',
            maxZoom: 19,
            maxNativeZoom: 19
        });
        const satelliteLabels = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            maxNativeZoom: 19,
            pane: 'overlayPane'
        });
        const streetsLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
            maxZoom: 19
        });

        satelliteBase.addTo(map);
        satelliteLabels.addTo(map);

        const toggleDiv = L.DomUtil.create('div');
        toggleDiv.style.display = 'flex';
        toggleDiv.style.gap = '4px';

        const btnSat = document.createElement('button');
        btnSat.textContent = 'Satellite';
        btnSat.className = 'px-2 py-1 text-xs font-medium rounded bg-blue-600 text-white shadow-sm focus:outline-none';
        btnSat.type = 'button';
        
        const btnStr = document.createElement('button');
        btnStr.textContent = 'Streets';
        btnStr.className = 'px-2 py-1 text-xs font-medium rounded bg-white text-gray-700 border border-gray-300 shadow-sm focus:outline-none hover:bg-gray-50';
        btnStr.type = 'button';

        toggleDiv.appendChild(btnSat);
        toggleDiv.appendChild(btnStr);

        const LayerToggleControl = L.Control.extend({
            options: { position: 'topright' },
            onAdd: function () {
                return toggleDiv;
            }
        });
        map.addControl(new LayerToggleControl());

        L.DomEvent.disableClickPropagation(toggleDiv);

        btnSat.addEventListener('click', (e) => {
            e.preventDefault();
            map.addLayer(satelliteBase);
            map.addLayer(satelliteLabels);
            map.removeLayer(streetsLayer);
            btnSat.className = 'px-2 py-1 text-xs font-medium rounded bg-blue-600 text-white shadow-sm focus:outline-none';
            btnStr.className = 'px-2 py-1 text-xs font-medium rounded bg-white text-gray-700 border border-gray-300 shadow-sm focus:outline-none hover:bg-gray-50';
        });

        btnStr.addEventListener('click', (e) => {
            e.preventDefault();
            map.removeLayer(satelliteBase);
            map.removeLayer(satelliteLabels);
            map.addLayer(streetsLayer);
            btnStr.className = 'px-2 py-1 text-xs font-medium rounded bg-blue-600 text-white shadow-sm focus:outline-none';
            btnSat.className = 'px-2 py-1 text-xs font-medium rounded bg-white text-gray-700 border border-gray-300 shadow-sm focus:outline-none hover:bg-gray-50';
        });

        L.rectangle(bounds, {
          color: '#4f46e5',
          weight: 2,
          dashArray: '5, 5',
          fillOpacity: 0.05
        }).addTo(map);

        const pickupIcon = new L.Icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });

        const dropoffIcon = new L.Icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });

        L.marker([pickupLat, pickupLon], { icon: pickupIcon }).addTo(map);
        L.marker([dropoffLat, dropoffLon], { icon: dropoffIcon }).addTo(map);

        // Draw polyline
        const latlngs = [
          [pickupLat, pickupLon],
          [dropoffLat, dropoffLon]
        ];
        L.polyline(latlngs, {color: '#4f46e5', weight: 4, dashArray: '5, 10'}).addTo(map);

        // Fit bounds to the two markers
        map.fitBounds(latlngs, { padding: [30, 30] });
      });
    });
}
