from django.shortcuts import get_object_or_404, render,get_list_or_404,redirect
from django.urls import reverse_lazy
from blog.models import Post,Comment
# Create your views here.
from django.views.generic import TemplateView,ListView,DeleteView,CreateView,DetailView,UpdateView,DeleteView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import CommentForm, PostForm


class AboutView(TemplateView):
    template_name='blog/about.html'

class Post_List_View(ListView):
    model=Post
    # It is just like filtering data,lte stands for less than or equal to ,- indicates descending order
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model=Post
    
# We use a CreateView when we need to implement a form  and after submission of form,the data should be saved to db.
# If the view is using loginrequiredmixin ,then all the requests from non authenticated users will be redirected to login url variable.
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='post_detail.html'
    form_class=PostForm
    model=Post
    # def get_success_url(self):
    #     return reverse_lazy('post_detail')
        

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model=Post
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    # author=post.author
    # title=post.title
    # text=post.text
    # created_date=post.created_date
    # published_date=post.published_date
    # import pdb;pdb.set_trace()
    if request.method=='POST':
        data=request.POST
        # import pdb;pdb.set_trace()
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment1=Comment(post=post,author=data['author'],text=data['text'],created_date=timezone.now(),approved_comment=False)
            # comment.post=post
            comment1.save()
            return redirect('post_detail',pk=post.pk)
        else:
            return redirect('post_detail',pk=post.pk)
    
    else:
        form=CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
