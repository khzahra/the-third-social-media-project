from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, LikePost, Comment
from django.utils.text import slugify
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib import messages
from .forms import PostUpdateForm, CommentCreateForm, CommentReplyForm
from home.forms import PostSearchForm

# Create your views here.


class CreatePostView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'post/create_post.html')

    def post(self, request):
        user = request.user
        title = request.POST['title']
        image = request.FILES.get('image')
        body = request.POST['body']
        slug = slugify(title[:50])

        new_post = Post.objects.create(user=user, title=title, image=image, body=body, slug=slug)
        new_post.save()

        return redirect('account:user_profile', request.user.id)




class PostDetailView(LoginRequiredMixin, View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(username=post.user)
        profile = Profile.objects.get(user=user)
        comments = post.post_comment.filter(is_reply=False)
        context = {
            'post': post,
            'user': user,
            'profile': profile,
            'comments': comments,
            'form': self.form_class,
            'reply_form': self.form_class_reply
        }
        return render(request, 'post/detail.html', context)

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post:post_detail', post_id)



class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Your post has been deleted successfully.', 'success')
        else:
            messages.error(request, 'You are not able to delete this post.', 'error')
        return redirect('account:user_profile', request.user.id)


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'You can not change this post.', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'post/update.html', {'form': form})
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            print('yes')
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:50])
            print(form.cleaned_data)
            # new_post.image.url = form.cleaned_data['image']
            new_post.save()
            messages.success(request, 'Post has been updated successfully.', 'success')
            return redirect('post:post_detail', post.id)
        messages.error(request, 'Try again.', 'danger')
        return render(request, 'post/update.html', {'form': form})



class ExploreView(LoginRequiredMixin,View):
    form_class = PostSearchForm
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'post/explore.html', {'posts': posts, 'form': self.form_class})


class LikePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user
        like_filter = LikePost.objects.filter(user=user, post=post)
        print(like_filter)
        if like_filter.exists():
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1
            post.save()
        else:
            new_like = LikePost.objects.create(user=user, post=post)
            new_like.save()
            post.no_of_likes = post.no_of_likes + 1
            post.save()
        return redirect('home:home')


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            return redirect('post:post_detail', post.id)
