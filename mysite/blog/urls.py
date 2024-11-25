from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from blog.views import AboutView, Post_List_View, CreatePostView, PostUpdateView, PostDetailView, PostDeleteView, DraftListView, comment_approve, DraftDetailView, post_publish
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Post_List_View.as_view(), name='post_list'),
    path('about/', AboutView.as_view(), name='about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/', PostDeleteView.as_view(), name='post_remove'),
    path('drafts/', DraftListView.as_view(), name='post_drafts'),  # Draft list view
    path('draft/<int:pk>/', DraftDetailView.as_view(), name='draft_detail'),
    path('draft/<int:pk>/publish/', post_publish, name='post_publish'),
    path('draft/<int:pk>/delete/', views.delete_draft_post, name='draft_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('contact/', views.contact_us, name='contact_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('accounts/login/',LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
