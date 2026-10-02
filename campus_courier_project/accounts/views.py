from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import FormView, View
from .models import Profile
from .forms import RegisterForm, ProfileForm


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully! Welcome to Campus Courier.")
        return redirect('dashboard')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        initial_data = {'email': request.user.email, 'phone': profile.phone}
        form = ProfileForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.phone = form.cleaned_data['phone']
            profile.save()
            
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


@login_required
@require_POST
def toggle_role_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.is_courier = not profile.is_courier
    profile.save()
    mode = "Courier" if profile.is_courier else "Sender"
    messages.success(request, f"Switched to {mode} mode.")
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'dashboard'
    return redirect(next_url)


ToggleRoleView = toggle_role_view
