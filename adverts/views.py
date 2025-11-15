"""
Views for adverts app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import Advert, Category
from .forms import AdvertForm
from .services import markdown_to_html


def advert_list(request):
    """List all published adverts with pagination and filters."""
    queryset = Advert.objects.filter(status=Advert.Status.PUBLISHED).select_related('author', 'category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            queryset = queryset.filter(category=category)
        except Category.DoesNotExist:
            pass
    
    # Search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(body_md__icontains=search_query)
        )
    
    # Order by created_at desc
    queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginate_by = getattr(settings, 'PAGINATE_BY', 15)
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    
    return render(request, 'adverts/list.html', context)


def advert_detail(request, pk):
    """Detail view for an advert."""
    advert = get_object_or_404(
        Advert.objects.select_related('author', 'category'),
        pk=pk,
        status=Advert.Status.PUBLISHED
    )
    
    context = {
        'advert': advert,
    }
    
    return render(request, 'adverts/detail.html', context)


@login_required
def advert_create(request):
    """Create a new advert."""
    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES)
        preview = request.POST.get('preview', False)
        
        if preview:
            # Preview mode - render Markdown without saving
            if form.is_valid():
                body_md = form.cleaned_data.get('body_md', '')
                
                # Process uploaded media files for preview
                image = form.cleaned_data.get('upload_image')
                video = form.cleaned_data.get('upload_video')
                
                if image or video:
                    # Convert files to base64 and insert into Markdown for preview
                    image_data_uri = None
                    video_data_uri = None
                    
                    if image:
                        image_data_uri = form._file_to_base64(image, 'image')
                    
                    if video:
                        video_data_uri = form._file_to_base64(video, 'video')
                    
                    # Insert media into body_md for preview
                    body_md = form._insert_media_to_markdown(body_md, image_data_uri, video_data_uri)
                
                body_html = markdown_to_html(body_md) if body_md else ''
                context = {
                    'form': form,
                    'preview_html': body_html,
                    'preview_data': form.cleaned_data,
                    'show_preview': True,  # Флаг для переключения на вкладку предпросмотра
                }
                return render(request, 'adverts/create.html', context)
        else:
            # Save mode
            if form.is_valid():
                advert = form.save(commit=False)
                advert.author = request.user
                advert.save()
                messages.success(request, 'Объявление успешно создано!')
                return redirect('adverts:detail', pk=advert.pk)
    else:
        form = AdvertForm()
    
    return render(request, 'adverts/create.html', {'form': form, 'show_preview': False})


@login_required
def advert_edit(request, pk):
    """Edit an existing advert."""
    advert = get_object_or_404(Advert, pk=pk)
    
    # Check if user is the author
    if advert.author != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого объявления.')
        return redirect('adverts:detail', pk=pk)
    
    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES, instance=advert)
        preview = request.POST.get('preview', False)
        
        if preview:
            # Preview mode
            if form.is_valid():
                body_md = form.cleaned_data.get('body_md', '')
                
                # Process uploaded media files for preview
                image = form.cleaned_data.get('upload_image')
                video = form.cleaned_data.get('upload_video')
                
                if image or video:
                    # Convert files to base64 and insert into Markdown for preview
                    image_data_uri = None
                    video_data_uri = None
                    
                    if image:
                        image_data_uri = form._file_to_base64(image, 'image')
                    
                    if video:
                        video_data_uri = form._file_to_base64(video, 'video')
                    
                    # Insert media into body_md for preview
                    body_md = form._insert_media_to_markdown(body_md, image_data_uri, video_data_uri)
                
                body_html = markdown_to_html(body_md) if body_md else ''
                context = {
                    'form': form,
                    'advert': advert,
                    'preview_html': body_html,
                    'preview_data': form.cleaned_data,
                    'show_preview': True,
                }
                return render(request, 'adverts/edit.html', context)
        else:
            # Save mode
            if form.is_valid():
                advert = form.save()
                messages.success(request, 'Объявление успешно обновлено!')
                return redirect('adverts:detail', pk=advert.pk)
    else:
        form = AdvertForm(instance=advert)
    
    return render(request, 'adverts/edit.html', {'form': form, 'advert': advert, 'show_preview': False})


@login_required
@require_http_methods(["POST"])
def advert_delete(request, pk):
    """Delete an advert."""
    advert = get_object_or_404(Advert, pk=pk)
    
    # Check if user is the author
    if advert.author != request.user:
        messages.error(request, 'У вас нет прав для удаления этого объявления.')
        return redirect('adverts:detail', pk=pk)
    
    advert.delete()
    messages.success(request, 'Объявление успешно удалено!')
    return redirect('adverts:list')



