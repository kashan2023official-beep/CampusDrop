import pytest
from orders.landmarks import CAMPUS_LANDMARKS, describe_location, find_nearest_landmark


def test_landmarks_list_has_minimum_entries():
    assert len(CAMPUS_LANDMARKS) >= 25


def test_find_nearest_landmark_exact_match():
    first = CAMPUS_LANDMARKS[0]
    result = find_nearest_landmark(first['lat'], first['lon'])
    assert result is not None
    assert result['name'] == first['name']


def test_find_nearest_landmark_within_threshold():
    first = CAMPUS_LANDMARKS[0]
    result = find_nearest_landmark(first['lat'] + 0.0005, first['lon'])
    assert result is not None


def test_find_nearest_landmark_beyond_threshold():
    first = CAMPUS_LANDMARKS[0]
    result = find_nearest_landmark(first['lat'] + 0.005, first['lon'])
    assert result is None


def test_describe_location_returns_landmark_name():
    first = CAMPUS_LANDMARKS[0]
    label, source = describe_location(first['lat'], first['lon'])
    assert label == first['name']
    assert source == 'landmark'


def test_describe_location_falls_back_to_coords():
    # 31.5825, 74.3525 is in the NW corner of the campus bounds, >150m away from landmarks
    label, source = describe_location(31.5825, 74.3525)
    assert source == 'coords'
    assert ',' in label


@pytest.mark.django_db
def test_reverse_geocode_requires_login(client):
    first = CAMPUS_LANDMARKS[0]
    response = client.get(f'/api/reverse-geocode/?lat={first["lat"]}&lon={first["lon"]}')
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_reverse_geocode_returns_landmark(client, sender_user):
    client.force_login(sender_user)
    first = CAMPUS_LANDMARKS[0]
    response = client.get(f'/api/reverse-geocode/?lat={first["lat"]}&lon={first["lon"]}')
    assert response.status_code == 200
    data = response.json()
    assert data['label'] == first['name']
    assert data['source'] == 'landmark'


@pytest.mark.django_db
def test_reverse_geocode_rejects_out_of_bounds(client, sender_user):
    client.force_login(sender_user)
    response = client.get('/api/reverse-geocode/?lat=40.0&lon=74.35')
    assert response.status_code == 400


@pytest.mark.django_db
def test_reverse_geocode_rejects_missing_params(client, sender_user):
    client.force_login(sender_user)
    response = client.get('/api/reverse-geocode/')
    assert response.status_code == 400


@pytest.mark.django_db
def test_reverse_geocode_rejects_bad_types(client, sender_user):
    client.force_login(sender_user)
    response = client.get('/api/reverse-geocode/?lat=abc&lon=74.35')
    assert response.status_code == 400


def test_find_nearest_landmark_at_120m_still_matches():
    """An offset of ~111m should still match since threshold is 150m."""
    L = CAMPUS_LANDMARKS[1]
    # +0.001 lat is ~111 meters north
    r = find_nearest_landmark(L['lat'] + 0.001, L['lon'])
    assert r is not None
    assert r['name'] == L['name']


@pytest.mark.django_db
def test_landmarks_json_endpoint(sender_user, client):
    """GET /api/landmarks/ returns 200 with all landmarks."""
    client.force_login(sender_user)
    r = client.get('/api/landmarks/')
    assert r.status_code == 200
    data = r.json()
    assert 'landmarks' in data
    assert len(data['landmarks']) >= 45
    for L in data['landmarks']:
        assert 'name' in L
        assert 'lat' in L
        assert 'lon' in L
        assert 'category' in L


@pytest.mark.django_db
def test_landmarks_json_endpoint_requires_login(client):
    """Anonymous GET /api/landmarks/ is blocked."""
    r = client.get('/api/landmarks/')
    assert r.status_code in (302, 403)

