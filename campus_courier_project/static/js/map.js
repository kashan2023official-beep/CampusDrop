
const state = { lastGeocodeId: 0 };

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
      btnSat.className = 'px-2 py-1 text-xs font-semibold rounded bg-brand-green text-brand-navy shadow-sm focus:outline-none';
      btnSat.type = 'button';
      
      const btnStr = document.createElement('button');
      btnStr.textContent = 'Streets';
      btnStr.className = 'px-2 py-1 text-xs font-medium rounded bg-white text-brand-navySubtext border border-brand-grey shadow-sm focus:outline-none hover:bg-brand-greySubtle';
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
          btnSat.className = 'px-2 py-1 text-xs font-semibold rounded bg-brand-green text-brand-navy shadow-sm focus:outline-none';
          btnStr.className = 'px-2 py-1 text-xs font-medium rounded bg-white text-brand-navySubtext border border-brand-grey shadow-sm focus:outline-none hover:bg-brand-greySubtle';
      });

      btnStr.addEventListener('click', (e) => {
          e.preventDefault();
          map.removeLayer(satelliteBase);
          map.removeLayer(satelliteLabels);
          map.addLayer(streetsLayer);
          btnStr.className = 'px-2 py-1 text-xs font-semibold rounded bg-brand-green text-brand-navy shadow-sm focus:outline-none';
          btnSat.className = 'px-2 py-1 text-xs font-medium rounded bg-white text-brand-navySubtext border border-brand-grey shadow-sm focus:outline-none hover:bg-brand-greySubtle';
      });

      L.rectangle(bounds, {
        color: '#03EF62',
        fillColor: '#03EF62',
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

      const landmarkToggleDiv = L.DomUtil.create('div');
      landmarkToggleDiv.className = 'leaflet-bar leaflet-control bg-white p-1';
      
      const btnLandmark = document.createElement('label');
      btnLandmark.className = 'flex items-center space-x-1 text-xs cursor-pointer p-1';
      btnLandmark.innerHTML = '<input type="checkbox" id="landmark-toggle" checked class="form-checkbox h-3 w-3 text-indigo-600 rounded"><span>Landmarks</span>';
      landmarkToggleDiv.appendChild(btnLandmark);

      const LandmarkControl = L.Control.extend({
          options: { position: 'topleft' },
          onAdd: function () {
              return landmarkToggleDiv;
          }
      });
      map.addControl(new LandmarkControl());
      L.DomEvent.disableClickPropagation(landmarkToggleDiv);

      const landmarkLayer = L.layerGroup().addTo(map);
      document.getElementById('landmark-toggle').addEventListener('change', (e) => {
          if (e.target.checked) {
              map.addLayer(landmarkLayer);
          } else {
              map.removeLayer(landmarkLayer);
          }
      });

      let currentMode = 'pickup';

      const buttons = document.querySelectorAll(opts.modeButtonsSelector);
      
      const updateButtonStates = () => {
        buttons.forEach(btn => {
          if (btn.dataset.mode === currentMode) {
            btn.className = 'px-3 py-1.5 text-sm font-semibold rounded-md bg-brand-green text-brand-navy shadow-sm hover:bg-brand-greenDark';
          } else {
            btn.className = 'px-3 py-1.5 text-sm font-medium rounded-md bg-white border border-brand-grey text-brand-navySubtext shadow-sm hover:bg-brand-greySubtle';
          }
        });
      };

      buttons.forEach(btn => {
        btn.addEventListener('click', () => {
          currentMode = btn.dataset.mode;
          updateButtonStates();
        });
      });

      const reverseGeocode = (lat, lon, labelInput) => {
        if (!labelInput) return;
        const requestId = ++state.lastGeocodeId;
        const url = `/api/reverse-geocode/?lat=${lat}&lon=${lon}`;
        fetch(url, { credentials: 'same-origin' })
          .then(r => r.ok ? r.json() : Promise.reject(r))
          .then(data => {
            if (requestId !== state.lastGeocodeId) return;      // discard stale
            if (labelInput.dataset.userEdited === '1') return;   // respect user edit
            labelInput.value = data.label;
            labelInput.dataset.source = data.source;             // 'landmark' or 'coords'
            // small visual cue
            labelInput.classList.remove('bg-brand-yellow/15', 'bg-brand-green/10', 'bg-yellow-50', 'bg-green-50');
            labelInput.classList.add(data.source === 'landmark' ? 'bg-brand-green/10' : 'bg-brand-yellow/15');
          })
          .catch(() => {
            if (requestId !== state.lastGeocodeId) return;
            if (labelInput.dataset.userEdited === '1') return;
            labelInput.value = `${lat.toFixed(5)}, ${lon.toFixed(5)}`;
          });
      };

      const updatePickup = (lat, lng) => {
        document.getElementById(opts.pickupLatId).value = lat;
        document.getElementById(opts.pickupLonId).value = lng;
        pickupMarker.setLatLng([lat, lng]);
        if (!isPickupSet) {
          pickupMarker.addTo(map);
          isPickupSet = true;
        }
        const labelInput = document.getElementById(opts.pickupLabelId) || document.getElementById('pickup_label');
        if (labelInput) labelInput.dataset.userEdited = '0';
        reverseGeocode(lat, lng, labelInput);
      };

      const updateDropoff = (lat, lng) => {
        document.getElementById(opts.dropoffLatId).value = lat;
        document.getElementById(opts.dropoffLonId).value = lng;
        dropoffMarker.setLatLng([lat, lng]);
        if (!isDropoffSet) {
          dropoffMarker.addTo(map);
          isDropoffSet = true;
        }
        const labelInput = document.getElementById(opts.dropoffLabelId) || document.getElementById('dropoff_label');
        if (labelInput) labelInput.dataset.userEdited = '0';
        reverseGeocode(lat, lng, labelInput);
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
          pickupMarker.setLatLng([parseFloat(initLat), parseFloat(initLon)]);
          if (!isPickupSet) {
              pickupMarker.addTo(map);
              isPickupSet = true;
          }
          const pLabel = document.getElementById(opts.pickupLabelId) || document.getElementById('pickup_label');
          if (pLabel && !pLabel.value) {
              reverseGeocode(parseFloat(initLat), parseFloat(initLon), pLabel);
          }
      }
      
      const initDLat = document.getElementById(opts.dropoffLatId).value;
      const initDLon = document.getElementById(opts.dropoffLonId).value;
      if (initDLat && initDLon) {
          dropoffMarker.setLatLng([parseFloat(initDLat), parseFloat(initDLon)]);
          if (!isDropoffSet) {
              dropoffMarker.addTo(map);
              isDropoffSet = true;
          }
          const dLabel = document.getElementById(opts.dropoffLabelId) || document.getElementById('dropoff_label');
          if (dLabel && !dLabel.value) {
              reverseGeocode(parseFloat(initDLat), parseFloat(initDLon), dLabel);
          }
      }

      // fetch landmarks and add to landmarkLayer
      fetch('/api/landmarks/')
        .then(r => r.json())
        .then(data => {
            data.landmarks.forEach(lm => {
                const marker = L.circleMarker([lm.lat, lm.lon], {
                    radius: 6,
                    color: '#00C74E',
                    fillColor: '#03EF62',
                    fillOpacity: 0.6,
                    weight: 2
                });
                
                const popupContent = document.createElement('div');
                popupContent.className = 'p-1';
                popupContent.innerHTML = `<p class="font-bold text-sm text-brand-navy mb-2">${lm.name}</p>
                  <div class="flex space-x-2">
                    <button class="set-pickup-btn px-2.5 py-1 bg-brand-green text-brand-navy font-semibold rounded text-xs shadow-sm hover:bg-brand-greenDark">Set as Pickup</button>
                    <button class="set-dropoff-btn px-2.5 py-1 bg-brand-red text-white font-semibold rounded text-xs shadow-sm hover:bg-brand-redDark">Set as Dropoff</button>
                  </div>`;
                
                popupContent.querySelector('.set-pickup-btn').addEventListener('click', () => {
                    updatePickup(lm.lat, lm.lon);
                    map.closePopup();
                    if (window.DEBUG_MAP) console.log('Landmark set as pickup:', lm.name);
                });
                popupContent.querySelector('.set-dropoff-btn').addEventListener('click', () => {
                    updateDropoff(lm.lat, lm.lon);
                    map.closePopup();
                    if (window.DEBUG_MAP) console.log('Landmark set as dropoff:', lm.name);
                });

                marker.bindPopup(popupContent);
                marker.bindTooltip(lm.name, {
                    direction: 'top',
                    offset: [0, -6],
                    opacity: 0.9,
                    sticky: false,
                });
                landmarkLayer.addLayer(marker);
            });
        });

    });
}
