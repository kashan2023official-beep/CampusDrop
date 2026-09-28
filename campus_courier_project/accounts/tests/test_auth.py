import pytest
from django.contrib.auth.models import User
from accounts.models import Profile


@pytest.mark.django_db
def test_register_creates_profile(client):
    """Creating a User auto-creates an associated Profile via signals."""
    user = User.objects.create_user(
        username='fresh_user',
        email='fresh@campus.local',
        password='Password123!',
    )
    assert hasattr(user, 'profile')
    assert isinstance(user.profile, Profile)
    assert user.profile.is_courier is False


@pytest.mark.django_db
def test_toggle_role_flips_is_courier(client, sender_user):
    """POST to /toggle-role/ toggles the is_courier boolean back and forth."""
    client.force_login(sender_user)
    assert sender_user.profile.is_courier is False

    response = client.post('/toggle-role/')
    assert response.status_code == 302
    sender_user.profile.refresh_from_db()
    assert sender_user.profile.is_courier is True

    response = client.post('/toggle-role/')
    assert response.status_code == 302
    sender_user.profile.refresh_from_db()
    assert sender_user.profile.is_courier is False


@pytest.mark.django_db
def test_login_required_redirect(client):
    """Unauthenticated access to protected view redirects to login page."""
    response = client.get('/profile/')
    assert response.status_code == 302
    assert '/login/' in response.url
