
export function initOrderMap(opts) {
  fetch('/api/campus-bounds/')
    .then(r => r.json())
    .then(data => {
      const bounds = data.bounds;
      const center = data.center;

      const map = L.map(opts.mapElId, {
        maxBounds: bounds,
        minZoom: 15,
        maxZoom: 19
      }).setView(center, 18);

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

      let pickupMarker = L.marker([0, 0], { icon: pickupIcon, draggable: true });
      let dropoffMarker = L.marker([0, 0], { icon: dropoffIcon, draggable: true });
      let isPickupSet = false;
      let isDropoffSet = false;

      let currentMode = 'pickup';

      const buttons = document.querySelectorAll(opts.modeButtonsSelector);
      
      const updateButtonStates = () => {
        buttons.forEach(btn => {
          if (btn.dataset.mode === currentMode) {
            btn.className = 'px-3 py-1.5 text-sm font-medium rounded-md bg-indigo-600 text-white shadow-sm hover:bg-indigo-700';
          } else {
            btn.className = 'px-3 py-1.5 text-sm font-medium rounded-md bg-white border border-gray-300 text-gray-700 shadow-sm hover:bg-gray-50';
          }
        });
      };

      buttons.forEach(btn => {
        btn.addEventListener('click', () => {
          currentMode = btn.dataset.mode;
          updateButtonStates();
        });
      });

      const simulateReverseGeocode = async (lat, lng) => {
        return new Promise(resolve => {
          setTimeout(() => {
            resolve(`Location ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
          }, 200);
        });
      };

      const updatePickup = async (lat, lng) => {
        document.getElementById(opts.pickupLatId).value = lat;
        document.getElementById(opts.pickupLonId).value = lng;
        pickupMarker.setLatLng([lat, lng]);
        if (!isPickupSet) {
          pickupMarker.addTo(map);
          isPickupSet = true;
        }
        const label = await simulateReverseGeocode(lat, lng);
        document.getElementById(opts.pickupLabelId).value = label;
      };

      const updateDropoff = async (lat, lng) => {
        document.getElementById(opts.dropoffLatId).value = lat;
        document.getElementById(opts.dropoffLonId).value = lng;
        dropoffMarker.setLatLng([lat, lng]);
        if (!isDropoffSet) {
          dropoffMarker.addTo(map);
          isDropoffSet = true;
        }
        const label = await simulateReverseGeocode(lat, lng);
        document.getElementById(opts.dropoffLabelId).value = label;
      };

      map.on('click', (e) => {
        const { lat, lng } = e.latlng;
        // Basic check if it's within bounds
        const leafletBounds = L.latLngBounds(bounds);
        if (!leafletBounds.contains(e.latlng)) {
          alert('Please select a location within the campus boundaries.');
          return;
        }

        if (currentMode === 'pickup') {
          updatePickup(lat, lng);
        } else {
          updateDropoff(lat, lng);
        }
      });

      pickupMarker.on('dragend', (e) => {
        const { lat, lng } = e.target.getLatLng();
        const leafletBounds = L.latLngBounds(bounds);
        if (!leafletBounds.contains(e.target.getLatLng())) {
          alert('Please stay within the campus boundaries.');
          // reset to previous? We just update with whatever it is or reset to bounds center? 
          // Simple for now: just update it, server will validate anyway. Or we can snap it.
        }
        updatePickup(lat, lng);
      });

      dropoffMarker.on('dragend', (e) => {
        const { lat, lng } = e.target.getLatLng();
        updateDropoff(lat, lng);
      });
      
      updateButtonStates();
      
      // If values are already set (e.g. form validation failure reload)
      const initLat = document.getElementById(opts.pickupLatId).value;
      const initLon = document.getElementById(opts.pickupLonId).value;
      if (initLat && initLon) {
          updatePickup(parseFloat(initLat), parseFloat(initLon));
      }
      
      const initDLat = document.getElementById(opts.dropoffLatId).value;
      const initDLon = document.getElementById(opts.dropoffLonId).value;
      if (initDLat && initDLon) {
          updateDropoff(parseFloat(initDLat), parseFloat(initDLon));
      }

    });
}
