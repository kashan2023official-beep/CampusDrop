import pytest


@pytest.mark.django_db
def test_staff_can_access(client, staff_user):
    """Staff user can successfully view the insights analytics dashboard."""
    client.force_login(staff_user)
    response = client.get('/insights/')
    assert response.status_code == 200
    assert b"Campus Insights" in response.content


@pytest.mark.django_db
def test_non_staff_blocked(client, sender_user):
    """Non-staff authenticated user is blocked and redirected to dashboard."""
    client.force_login(sender_user)
    response = client.get('/insights/')
    # staff_required decorator redirects non-staff users
    assert response.status_code in (302, 403)
    if response.status_code == 302:
        assert '/dashboard/' in response.url


@pytest.mark.django_db
def test_anonymous_redirected(client):
    """Anonymous user is redirected to the login page."""
    response = client.get('/insights/')
    assert response.status_code == 302
    assert '/login/' in response.url
