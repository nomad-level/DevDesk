from django.db import models


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('bug', 'Bug'),
        ('css', 'CSS'),
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Database'),
        ('deployment', 'Deployment'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('solved', 'Solved'),
    ]
    
    title = models.CharField(max_length=200)
    assign = models.CharField(max_length=100, default='Public')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    email = models.EmailField(blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return self.title
    
    def get_participants_emails(self):
        emails = set([self.email])
        for _comment in self.comments.all():
            pass
        return list(emails)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_created']
    
    def __str__(self):
        return f'Comment by {self.name or "Anonymous"} on {self.post.title}'
