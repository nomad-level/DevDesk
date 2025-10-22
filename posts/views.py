from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.all()
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        posts = posts.filter(status=status)
    
    context = {
        'posts': posts,
        'categories': Post.CATEGORY_CHOICES,
        'statuses': Post.STATUS_CHOICES,
        'selected_category': category,
        'selected_status': status,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
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
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


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

