import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import haversine_distances

def compute_hotspots(min_samples=4, eps_km=0.15) -> list[dict]:
    from orders.models import Order
    from orders.landmarks import find_nearest_landmark

    orders = list(Order.objects.filter(status__in=['PICKED_UP', 'DELIVERED']).values('id', 'pickup_lat', 'pickup_lon'))
    if not orders:
        return []

    coords = np.array([[o['pickup_lat'], o['pickup_lon']] for o in orders])
    coords_rad = np.radians(coords)
    kms_per_radian = 6371.0088

    db = DBSCAN(eps=eps_km / kms_per_radian, min_samples=min_samples, metric='haversine', algorithm='ball_tree')
    labels = db.fit_predict(coords_rad)

    unique_labels = set(labels)
    hotspots = []

    for label in unique_labels:
        if label == -1:
            continue

        cluster_mask = (labels == label)
        cluster_coords_rad = coords_rad[cluster_mask]
        
        centroid_rad = np.mean(cluster_coords_rad, axis=0)
        centroid_deg = np.degrees(centroid_rad)
        centroid_lat, centroid_lon = centroid_deg[0], centroid_deg[1]

        # Calculate max distance from centroid in km
        # haversine_distances takes (n_samples, 2) in radians
        dists = haversine_distances([centroid_rad], cluster_coords_rad)[0]
        max_dist_km = np.max(dists) * kms_per_radian

        # Find landmark
        landmark = find_nearest_landmark(centroid_lat, centroid_lon, max_distance_m=300)
        landmark_label = landmark['name'] if landmark else "Zone"

        hotspots.append({
            'centroid_lat': float(centroid_lat),
            'centroid_lon': float(centroid_lon),
            'radius_km': float(max_dist_km),
            'count': int(np.sum(cluster_mask)),
            'label': landmark_label,
        })

    hotspots.sort(key=lambda x: x['count'], reverse=True)
    return hotspots

def hotspots_available() -> bool:
    from orders.models import Order
    return Order.objects.filter(status__in=['PICKED_UP', 'DELIVERED']).count() >= 10
