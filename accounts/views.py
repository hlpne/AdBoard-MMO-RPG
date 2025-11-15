"""
Views for accounts app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_http_methods
from .models import User, EmailVerification
from .forms import SignupForm, VerifyForm, LoginForm
from .services import send_verification_email


def signup(request):
    """User signup view."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create verification code
            code = EmailVerification.generate_code()
            expires_at = timezone.now() + timedelta(minutes=30)
            verification = EmailVerification.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            # Send verification email
            send_verification_email(user, code)
            messages.success(request, 'Регистрация успешна! Проверьте почту для подтверждения email.')
            return redirect('accounts:verify', user_id=user.id)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def verify(request, user_id):
    """Email verification view."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return redirect('accounts:signup')
    
    if user.is_active:
        messages.info(request, 'Ваш email уже подтверждён.')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = VerifyForm(request.POST, user=user)
        if form.is_valid():
            code = form.cleaned_data['code']
            verification = EmailVerification.objects.get(user=user, code=code, is_used=False)
            verification.is_used = True
            verification.save()
            
            user.is_active = True
            user.save()
            
            messages.success(request, 'Email успешно подтверждён! Теперь вы можете войти.')
            return redirect('accounts:login')
    else:
        form = VerifyForm(user=user)
    
    return render(request, 'accounts/verify.html', {'form': form, 'user': user})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.email}!')
            next_url = request.GET.get('next', '/adverts/')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """User profile view."""
    user = request.user
    # Get or create profile
    from .models import UserProfile
    profile_obj, created = UserProfile.objects.get_or_create(user=user)
    
    # Get user statistics
    from adverts.models import Advert
    from replies.models import Reply
    
    user_adverts_count = Advert.objects.filter(author=user).count()
    user_replies_count = Reply.objects.filter(author=user).count()
    
    context = {
        'user': user,
        'profile': profile_obj,
        'user_adverts_count': user_adverts_count,
        'user_replies_count': user_replies_count,
    }
    
    return render(request, 'accounts/profile.html', context)

