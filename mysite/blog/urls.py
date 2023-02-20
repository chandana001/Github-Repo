from django.contrib import admin
from django.urls import path,include
from blog.views import AboutView,Post_List_View,CreatePostView,PostUpdateView, PostDetailView,PostDeleteView,DraftListView, comment_approve
from blog import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('blog/', include('blog.urls')),
    path('', Post_List_View.as_view(template_name='blog/post_list.html'), name='post_list'),
    path('about/', AboutView.as_view(), name='about'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/new/',CreatePostView.as_view(),name='post_new'),
    path('post/<int:pk>/edit/',PostUpdateView.as_view(template_name='blog/post_form.html'),name='post_edit'),
    path('post/<int:pk>/remove/',PostDeleteView.as_view(),name='post_remove'),
    path('drafts/',DraftListView.as_view(),name='post_draft_list'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve/',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove/',views.comment_remove,name='comment_remove'),
    path('post/<int:pk>/publish/',views.post_publish,name='post_publish'),
]