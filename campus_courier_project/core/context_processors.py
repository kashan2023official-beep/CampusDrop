def role_mode(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        return {'current_mode': 'courier' if request.user.profile.is_courier else 'sender'}
    return {'current_mode': 'sender'}
