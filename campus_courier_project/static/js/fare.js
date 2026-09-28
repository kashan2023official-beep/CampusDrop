document.addEventListener('DOMContentLoaded', () => {
    const preview = document.getElementById('fare-preview');
    if (!preview) return;

    const weightInput = document.getElementById('id_weight_kg');
    const typeInput = document.getElementById('id_item_type');
    
    // Hidden inputs from map
    const pLat = document.getElementById('id_pickup_lat');
    const pLon = document.getElementById('id_pickup_lon');
    const dLat = document.getElementById('id_dropoff_lat');
    const dLon = document.getElementById('id_dropoff_lon');

    let debounceTimer;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateFare() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const distance = parseFloat(preview.dataset.distanceKm) || 0;
            if (distance <= 0) {
                preview.style.display = 'none';
                return;
            }
            preview.style.display = 'block';

            const weight = parseFloat(weightInput.value);
            const itemType = typeInput.value;

            if (!weight || !itemType) {
                preview.textContent = "≈ — PKR";
                return;
            }

            preview.classList.add('animate-pulse');
            fetch('/api/predict-fare/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    distance_km: distance,
                    weight_kg: weight,
                    item_type: itemType
                })
            })
            .then(res => {
                if (res.ok) return res.json();
                throw new Error('Fare unavailable');
            })
            .then(data => {
                preview.textContent = `≈ ${data.fare} PKR`;
            })
            .catch(err => {
                preview.textContent = 'Fare unavailable';
            })
            .finally(() => {
                preview.classList.remove('animate-pulse');
            });
        }, 400);
    }

    if (weightInput && typeInput) {
        weightInput.addEventListener('input', updateFare);
        typeInput.addEventListener('change', updateFare);
    }

    let lastDistanceState = '';
    setInterval(() => {
        if (pLat && pLon && dLat && dLon && pLat.value && pLon.value && dLat.value && dLon.value) {
            const currentState = `${pLat.value},${pLon.value}-${dLat.value},${dLon.value}`;
            if (currentState !== lastDistanceState) {
                lastDistanceState = currentState;
                fetch(`/api/estimate-distance/?pickup_lat=${pLat.value}&pickup_lon=${pLon.value}&dropoff_lat=${dLat.value}&dropoff_lon=${dLon.value}`)
                    .then(r => r.json())
                    .then(data => {
                        if (data.distance_km) {
                            preview.dataset.distanceKm = data.distance_km;
                            updateFare();
                        }
                    });
            }
        }
    }, 500);

    updateFare();
});
