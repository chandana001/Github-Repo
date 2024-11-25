from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from blog.models import Post,Comment
from django.db.models import Q
# Create your views here.
from django.views.generic import TemplateView,ListView,DeleteView,CreateView,DetailView,UpdateView,DeleteView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import CommentForm, PostForm

# About View
class AboutView(TemplateView):
    template_name = 'blog/about.html'

# Post List View: Show published posts
class Post_List_View(ListView):
    model = Post
    template_name = "blog/post_list.html"  

    def get_queryset(self):
        query = self.request.GET.get('q')  
        queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))  # Filter by title
        return queryset

# Post Detail View: View individual post details
class PostDetailView(DetailView):
    model = Post

# Create Post View: Handle the creation of a post
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user 
        form.save() 
       
        messages.success(self.request, "Your post has been created successfully!")

        
        return redirect('post_list')
# Update Post View: Edit an existing post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'  
    success_url = '/' 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Delete Post View: Delete a post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


def delete_draft_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the post is a draft
    if post.published_date is None:
        if request.method == "POST":
            post.delete()
            messages.success(request, "Post has been deleted successfully.")
            return redirect('post_drafts')  # redirect back to the draft list view
        
        return render(request, 'blog/draft_post_confirm_delete.html', {'post': post})
    
    else:
        
        messages.error(request, "You can't delete a published post.")
        return redirect('post_drafts')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'blog/post_drafts.html'  # Ensure this matches your template file
    model = Post

    def get_queryset(self):
        # Filter to show only drafts (published_date is null)
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

# Draft Detail View: View the details of a draft post
class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/draft_detail.html'

    def get_object(self):
        post = super().get_object()
        if post.published_date is not None:
            raise Http404("This post is already published.")
        return post

# Add a Comment to a Post
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        data = request.POST
        if form.is_valid():
            comment=form.save(commit=False)
            comment1=Comment(post=post,author=request.user,text=data['text'],created_date=timezone.now(),approved_comment=False)
            # comment.post=post
            comment1.save()
            

            # Show success message
            messages.success(request, "Your comment has been posted successfully!")
            return redirect('post_detail', pk=post.pk)  
        else:
            messages.error(request, "There was an error with your comment submission.")
    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})

# Approve Comment (Admin functionality)
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    print(comment)
    comment.approve()

    
    messages.success(request, 'Your comment has been approved!')

    return redirect('post_detail', pk=comment.post.pk)

# Remove Comment
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    
    messages.success(request, 'Your comment has been removed!')

    return redirect('post_detail', pk=post_pk)

# Publish a Post (Make a draft post public)
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)

   
    post.published_date = timezone.now()
    post.save()

    
    messages.success(request, 'Your post has been published!')

    
    return redirect('post_detail', pk=post.pk)

# Contact Us Page
def contact_us(request):
    message_sent = False
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        message_sent = True

    return render(request, 'blog/contact_us.html', {'message_sent': message_sent})

# Privacy Policy Page
def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

# Terms of Service Page
def terms_of_service(request):
    return render(request, 'blog/terms_of_service.html')
