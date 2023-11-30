from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('detail/<int:post_id>', views.PostDetailView.as_view(), name='post_detail'),
    path('delete/<int:post_id>', views.PostDeleteView.as_view(), name='post_delete'),
    path('upadte/<int:post_id>', views.PostUpdateView.as_view(), name='post_update'),
    path('explore', views.ExploreView.as_view(), name='explore'),
    path('like/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    path('reply/<int:post_id>/<int:comment_id>/', views.PostAddReplyView.as_view(), name='add_reply'),
]