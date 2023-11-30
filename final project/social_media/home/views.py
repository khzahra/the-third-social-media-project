from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from account.models import Profile, Relation
from post.models import Post
from itertools import chain
from .forms import PostSearchForm


# Create your views here.


class HomeView(LoginRequiredMixin, View):
    form_class = PostSearchForm
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user)

        user_following = Relation.objects.filter(from_user=user)

        user_following_list = []
        for users in user_following:
            user_following_list.append(users.to_user)

        feed_list = []
        for users in user_following_list:
            feed = Post.objects.filter(user=users)
            feed_list.append(feed)

        post_list = list(chain(*feed_list))

        if request.GET.get('search'):
            all_posts = Post.objects.all()
            post_list = all_posts.filter(body__contains=request.GET['search'])

        context = {'user': user, 'user_profile': user_profile, 'feed': post_list, 'form': self.form_class}

        return render(request, 'home/index.html', context)
