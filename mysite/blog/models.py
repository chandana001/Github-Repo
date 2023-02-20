from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now())
    published_date=models.DateTimeField(blank=True,null=True)
    
    # Authorised Users can publish
    def publish(self):
        self.published_date=timezone.now()
        self.save()

    # Authorised Users can comment
    def approve_comments(self):
        return self.comments.filter(approved_comments=True)
    
    # I think it will show post and the comments
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})



    def __str__(self):
        return self.title

class Comment(models.Model):
    
    # Blog Post is a model ,so this field is connected to other model
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    #why don't we take author from auth.user because any one can comment not only authorised user
    # Any person can comment So,we are not taking it from auth.User
    author=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now())
    approved_comment=models.BooleanField(default=False)
   
    # have to know this method
    # If the authorised user,can approve or cannot approve
    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        # It will be the list of all posts that will be visible on homepage
        return reverse('post_list')


    def __str__(self):
        return self.text