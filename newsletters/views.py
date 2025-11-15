"""
Views for newsletters app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Subscription, NewsletterTemplate, NewsletterSendJob
from .services import subscribe_user, unsubscribe_user


@login_required
@require_http_methods(["POST"])
def subscribe(request):
    """Subscribe user to newsletter."""
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        defaults={'is_active': True}
    )
    
    if not created and subscription.is_active:
        messages.info(request, 'Вы уже подписаны на рассылку.')
    else:
        subscription.is_active = True
        subscription.save()
        messages.success(request, 'Вы успешно подписались на рассылку!')
    
    next_url = request.POST.get('next', '/adverts/')
    return redirect(next_url)


@login_required
@require_http_methods(["POST"])
def unsubscribe(request):
    """Unsubscribe user from newsletter."""
    try:
        subscription = Subscription.objects.get(user=request.user)
        subscription.is_active = False
        subscription.save()
        messages.success(request, 'Вы отписались от рассылки.')
    except Subscription.DoesNotExist:
        messages.info(request, 'Вы не были подписаны на рассылку.')
    
    next_url = request.POST.get('next', '/adverts/')
    return redirect(next_url)


@user_passes_test(lambda u: u.is_staff)
def template_list(request):
    """List newsletter templates (admin only)."""
    templates = NewsletterTemplate.objects.all()
    return render(request, 'newsletters/template_list.html', {'templates': templates})


@user_passes_test(lambda u: u.is_staff)
def send_newsletter_view(request, template_id):
    """Initiate newsletter send (admin only)."""
    template = get_object_or_404(NewsletterTemplate, pk=template_id)
    
    if request.method == 'POST':
        # Create send job
        job = NewsletterSendJob.objects.create(
            template=template,
            status=NewsletterSendJob.Status.QUEUED
        )
        
        # Start sending (this will be handled by APScheduler or management command)
        from .services import send_newsletter_batch
        # For now, process synchronously (in production, use APScheduler)
        try:
            send_newsletter_batch(template.id, batch_size=50, delay=2)
            messages.success(request, f'Рассылка "{template.title}" запущена!')
        except Exception as e:
            messages.error(request, f'Ошибка при отправке рассылки: {e}')
        
        return redirect('newsletters:template_list')
    
    return render(request, 'newsletters/send_newsletter.html', {'template': template})

