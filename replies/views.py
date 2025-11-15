"""
Views for replies app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.db import transaction
from django.utils import timezone as tz
from .models import Reply
from .forms import ReplyForm
from .services import send_reply_notification, send_accept_notification
from adverts.models import Advert


@login_required
@require_http_methods(["POST"])
def reply_create(request):
    """Create a new reply to an advert."""
    advert_id = request.POST.get('advert_id')
    advert = get_object_or_404(Advert, pk=advert_id, status=Advert.Status.PUBLISHED)
    
    # Check if user is trying to reply to their own advert
    if advert.author == request.user:
        messages.error(request, 'Вы не можете оставить отклик на своё объявление.')
        return redirect('adverts:detail', pk=advert.pk)
    
    form = ReplyForm(request.POST, advert=advert, user=request.user)
    
    if form.is_valid():
        reply = form.save(commit=False)
        reply.advert = advert
        reply.author = request.user
        
        with transaction.atomic():
            reply.save()
            # Send notification email to advert author
            send_reply_notification(reply)
        
        messages.success(request, 'Отклик успешно отправлен!')
        return redirect('adverts:detail', pk=advert.pk)
    else:
        messages.error(request, 'Ошибка при создании отклика.')
        return redirect('adverts:detail', pk=advert.pk)


@login_required
def my_replies(request):
    """List replies to user's adverts."""
    # Get all adverts owned by the user
    user_adverts = Advert.objects.filter(author=request.user)
    
    # Get replies to user's adverts
    queryset = Reply.objects.filter(
        advert__in=user_adverts
    ).select_related('advert', 'author', 'advert__category')
    
    # Filter by advert
    advert_id = request.GET.get('advert')
    if advert_id:
        try:
            advert = Advert.objects.get(pk=advert_id, author=request.user)
            queryset = queryset.filter(advert=advert)
        except Advert.DoesNotExist:
            pass
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)
    
    # Search by text
    search_query = request.GET.get('q', '').strip()
    if search_query:
        queryset = queryset.filter(text__icontains=search_query)
    
    # Order by created_at desc
    queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginate_by = getattr(settings, 'PAGINATE_BY', 15)
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get user's adverts for filter
    user_adverts_list = user_adverts.order_by('-created_at')
    
    context = {
        'page_obj': page_obj,
        'user_adverts': user_adverts_list,
        'current_advert': int(advert_id) if advert_id and advert_id.isdigit() else None,
        'current_status': status,
        'search_query': search_query,
    }
    
    return render(request, 'replies/my_replies.html', context)


@login_required
@require_http_methods(["POST"])
def reply_accept(request, pk):
    """Accept a reply."""
    reply = get_object_or_404(Reply, pk=pk)
    
    # Check if user is the owner of the advert
    if reply.advert.author != request.user:
        messages.error(request, 'У вас нет прав для принятия этого отклика.')
        return redirect('replies:my_replies')
    
    # Check if reply is not already accepted or deleted
    if reply.status == Reply.Status.ACCEPTED:
        messages.info(request, 'Этот отклик уже принят.')
        return redirect('replies:my_replies')
    
    if reply.status == Reply.Status.DELETED:
        messages.error(request, 'Нельзя принять удалённый отклик.')
        return redirect('replies:my_replies')
    
    with transaction.atomic():
        reply.status = Reply.Status.ACCEPTED
        reply.save()
        # Send notification email to reply author
        send_accept_notification(reply)
    
    messages.success(request, 'Отклик принят! Автор отклика получит уведомление.')
    return redirect('replies:my_replies')


@login_required
@require_http_methods(["POST"])
def reply_delete(request, pk):
    """Delete a reply (soft delete)."""
    reply = get_object_or_404(Reply, pk=pk)
    
    # Check if user is the owner of the advert
    if reply.advert.author != request.user:
        messages.error(request, 'У вас нет прав для удаления этого отклика.')
        return redirect('replies:my_replies')
    
    # Soft delete
    reply.status = Reply.Status.DELETED
    reply.deleted_at = tz.now()
    reply.save()
    
    messages.success(request, 'Отклик удалён.')
    return redirect('replies:my_replies')

