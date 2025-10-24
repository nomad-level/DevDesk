from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Comment
from .forms import PostForm, CommentForm
import uuid


def post_list(request):
    posts = Post.objects.all()
    
    # Get or create session ID
    session_id = request.COOKIES.get('devdesk_session_id')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        posts = posts.filter(status=status)
    
    # Filter by "my posts"
    my_posts = request.GET.get('my_posts')
    if my_posts and session_id:
        posts = posts.filter(session_id=session_id)
    
    context = {
        'posts': posts,
        'categories': Post.CATEGORY_CHOICES,
        'statuses': Post.STATUS_CHOICES,
        'selected_category': category,
        'selected_status': status,
        'show_my_posts': my_posts,
        'session_id': session_id,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    # Get or create session ID
    session_id = request.COOKIES.get('devdesk_session_id')
    is_owner = (session_id and post.session_id == session_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            
            # Send email notifications
            send_comment_notifications(post, comment)
            
            messages.success(request, 'Your comment has been posted!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'is_owner': is_owner,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            # Get or create session ID
            session_id = request.COOKIES.get('devdesk_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
            
            post.session_id = session_id
            post.save()
            
            messages.success(request, 'Your post has been created successfully!')
            response = redirect('post_detail', pk=post.pk)
            response.set_cookie('devdesk_session_id', session_id, max_age=365*24*60*60)  # 1 year
            return response
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


def post_edit(request, pk):
    """Edit an existing post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user owns this post
    session_id = request.COOKIES.get('devdesk_session_id')
    if not session_id or post.session_id != session_id:
        messages.error(request, 'You can only edit your own posts!')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'posts/post_edit.html', context)


def post_delete(request, pk):
    """Delete a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user owns this post
    session_id = request.COOKIES.get('devdesk_session_id')
    if not session_id or post.session_id != session_id:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post has been deleted successfully!')
        return redirect('post_list')
    return redirect('post_detail', pk=pk)


def comment_delete(request, pk):
    """Delete a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment has been deleted successfully!')
    return redirect('post_detail', pk=post_pk)


def send_comment_notifications(post, comment):
    """Send an email notification when a new comment is added."""
    emails = set([post.email])
    
    for prev_comment in post.comments.exclude(pk=comment.pk):
        pass
    
    if emails:
        subject = f'New comment on: {post.title}'
        message = f'''
Hello,

A new comment has been added to the post "{post.title}".

Commenter: {comment.name or "Anonymous"}
Comment: {comment.body[:200]}...

View the full discussion at: http://localhost:8000/post/{post.pk}/

---
DevDesk - Developer Issue Tracker
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                list(emails),
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

