from django.shortcuts import redirect
from django.views import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('login')
